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
        
        elif self.strategy == "self_refine":
            return self.solve_self_refine(prompt)
        
        elif self.strategy == "CoT":
            return self.solve_chain_of_thought(prompt)

    def solve_baseline(self, input):
        result = call_model_chat_completions(input, system= (
            """
            You are a careful problem solver. Give ONLY the final answer and it should not exceed 5000 characters.
            Do NOT provide any explanations, steps, or additional text.
            Give final answer for numerical questions or the expression if the question asks for expression.
            For yes/no questions, respond only with 'true' or 'false'.
            If a question is multiple choice, respond ONLY with answer text.
            """
        ))
        if result["ok"]:
            return (result["text"] or "").strip()
        return ""
    
    # strategy 1: self consistency
    def solve_self_consistency(self, input, n=7):
        """
        self consistency is a method where we get multiple CoT paths and we choose the majority voting. 
        References say it is good for math and common sense domains.
        input is the prompt and n is the number of CoT samples. (in this case, n = 7)
        ALWAYS give the final answer and should not exceed 4000 characters.
        """
        cot_answers = []
        for _ in range(n):
            result = call_model_chat_completions(input, system=(
                """
                You are a careful problem solver. Give ONLY the final answer and it should not exceed 5000 characters.
                Do NOT provide any explanations, steps, or additional text.
                Give final answer for numerical questions or the expression if the question asks for expression.
                For yes/no questions, respond only with 'true' or 'false'.
                If a question is multiple choice, respond ONLY with answer text.
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

    # strateg 2: self refine
    def solve_self_refine(self, input):
        """
        Self refine - In this method, I use model 3 times:
        - Initial attempt to answer the question
        - Critique step where the model critiques and provides feedback on the initial answer
        - Refinement step where the model uses the critique to improve the answer and give a final answer.
        """
        # initial attempt to answer the question
        initial_attempt = call_model_chat_completions(input, system=(
            """
            You are a careful problem solver. Give ONLY the final answer and it should not exceed 5000 characters.
            Do NOT provide any explanations, steps, or additional text.
            Give final answer for numerical questions or the expression if the question asks for expression.
            For yes/no questions, respond only with 'true' or 'false'.
            If a question is multiple choice, respond ONLY with answer text.
            """
        ), temperature=0.4)

        if not initial_attempt["ok"]:
            return ""
        
        initial_answer = (initial_attempt["text"] or "").strip()

        # critique step
        critique = call_model_chat_completions(f"""Here is the initial answer: {initial_answer}. Give feedback on what could be wrong with this answer and how to improve it.""", 
                                               system=( 
                                                   """You are an expert critic. Provide constructive feedback on the provided answer, check for any mistakes in calculations, logic, coding, or reasoning and provide suggestions for improvements."""
                                                ), temperature=0.4)

        critique_text = ""
        if critique["ok"]:
            critique_text = (critique["text"] or "").strip()
        
        # refinement step
        refined_answer = call_model_chat_completions(f"""For the question: {input}, here is the initial answer: {initial_answer}. Here is the critique with feedback: {critique_text}. Based on this critique, provide a refined final answer.""",
                                              system=(
                                                  """You are a careful problem solver. Give ONLY the final answer and it should not exceed 5000 characters.
                                                       Do NOT provide any explanations, steps, or additional text.
                                                       Give final answer for numerical questions or the expression if the question asks for expression.
                                                       For yes/no questions, respond only with 'true' or 'false'.
                                                       If a question is multiple choice, respond ONLY with answer text.
                                                    """
                                              ), temperature=0.1)
        
        if refined_answer["ok"]:
            return (refined_answer["text"] or "").strip()
        return ""

    # strategy 3: Chain of Thought (CoT) prompting
    def solve_chain_of_thought(self, input):
        """
        In Chain of Thought, I call the model twice:
        - First to generate the reasoning steps
        - Then, I get the final answer based on the reasoning steps, and the format specified in the quesiton.
        """
        # thinking step
        cot_result = call_model_chat_completions(f"""For question: {input}, think step by step to solve the problem.""",
                                          system=(
                                              """
                                              You are a careful problem solver. Think step by step to solve the problem but do NOT provide the final answer yet.
                                              Reply with your reasoning steps only.
                                              """
                                            ), temperature=0.4)

        if not cot_result["ok"]:
            return ""
        
        cot_reasoning = (cot_result["text"] or "").strip()

        # final answer step
        final_answer_result = call_model_chat_completions(f"""Based on the following reasoning steps: {cot_reasoning}, provide ONLY the final answer to the question: {input}. """,
                                                system=(
                                                    """You are a careful problem solver. Give ONLY the final answer and it should not exceed 5000 characters.
                                                       Do NOT provide any explanations, steps, or additional text.
                                                       Give final answer for numerical questions or the expression if the question asks for expression.
                                                       For yes/no questions, respond only with 'true' or 'false'.
                                                       If a question is multiple choice, respond ONLY with answer text.
                                                    """
                                                ), temperature=0.1)

        if final_answer_result["ok"]:
            return (final_answer_result["text"] or "").strip()
        return ""