from model.api import call_model_chat_completions

class Agent:
    def __init__(self, strategy="baseline"):
        self.strategy = strategy
    
    def solve(self, prompt):
        if self.strategy == "baseline":
            return self.solve_baseline(prompt)

    def solve_baseline(self, input):
        result = call_model_chat_completions(input)
        if result["ok"]:
            return (result["text"] or "").strip()
        return ""