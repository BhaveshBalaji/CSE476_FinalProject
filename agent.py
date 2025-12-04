from model.api import call_model_chat_completions

class Agent:
    def __init__(self, strategy="baseline"):
        self.strategy = strategy
    
    def solve(self, prompt):
        if self.strategy == "baseline":
            return self.solve_baseline(prompt)

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