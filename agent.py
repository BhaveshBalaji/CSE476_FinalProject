from model.api import call_model_chat_completions
from utils import normalize_text
from collections import Counter # self consistency majority voting

class Agent:
    def __init__(self, strategy="baseline"):
        self.strategy = strategy
    
    def solve(self, prompt):
        if self.strategy == "baseline":
            return self.solve_baseline(prompt)

        elif self.strategy == "self_consistency":
            return self.solve_self_consistency(prompt)

    def solve_baseline(self, input):
        result = call_model_chat_completions(input, system= (
            """
            You are a careful problem solver. Reply with ONLY the final answer.
            Do NOT provide any explanations, steps, or additional text.
            If the question is numeric, respond with just the final answer number.
            For yes/no questions, respond only with 'true' or 'false'.
            If the question has specified answer format, adhere to it strictly.
            """
        ))
        if result["ok"]:
            return (result["text"] or "").strip()
        return ""
    
    def solve_self_consistency(self, input, n=7):
        """
        self consistency is a method where we get multiple CoT paths and we choose the majority voting. 
        References say it is good for math and common sense domains.
        input is the prompt and n is the number of CoT samples. (in this case, n = 7)
        """
        cot_answers = []
        for _ in range(n):
            result = call_model_chat_completions(input, system=(
                """
                You are a careful problem solver. Reply with ONLY the final answer.
                Do NOT provide any explanations, steps, or additional text.
                If the question is numeric, respond with just the final numeric answer or expression if the question ask for the expression.
                For yes/no questions, respond only with 'true' or 'false'.
                If a question is multiple choice, respond ONLY with the answer text, DO NOT include the choice label like '1)', '3)', 'A)', 'B)', etc.
                If the question has specified answer format, adhere to it strictly.
                """
            ),
            temperature=0.7 # self consistency requires temperature > 0, and higher temperature gives diverse samples.
            )

            if result["ok"]:
                raw_answer = (result["text"] or "").strip()
                normalized_answer = normalize_text(raw_answer)
                cot_answers.append(normalized_answer)
        
        # handle if no answers were obtained.
        if not cot_answers:
            return ""
        
        # I would use Counter to get majority vote answer. (Counter.most_common())
        counter = Counter(cot_answers)
        majority_answer = counter.most_common(1)[0][0]
        return majority_answer
