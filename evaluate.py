import json
import time
from agent import Agent
from pathlib import Path
from typing import Any, Dict, List
from utils import normalize_text

"""
Intuition: I created this file to evaluate the accuracy of model with different inference
time methods or strategies starting with baseline (no method used, just testing
how good the model is).
"""

def grade(expected: str, got: str) -> bool:
    return normalize_text(got) == normalize_text(expected)

def load_dev_data(path: Path) -> List[Dict[str, Any]]:
    with path.open("r") as fp:
        data = json.load(fp)
    if not isinstance(data, list):
        raise ValueError("Input file must contain a list of question objects.")
    return data

def evaluate(dev_data, strategy):
    agent = Agent(strategy=strategy)

    results = []
    correct_per_domain = {}
    total_per_domain = {}

    print(f"Evaluation started with strategy: {strategy}")
    for item in dev_data:
        input = item.get("input")
        target = item.get("output")
        domain = item.get("domain")

        if domain not in total_per_domain:
            total_per_domain[domain] = 0
            correct_per_domain[domain] = 0
        
        total_per_domain[domain] += 1

        # get model response
        prediction = agent.solve(input)

        is_correct = grade(target, prediction)
        if is_correct:
            correct_per_domain[domain] += 1

        results.append({
            "input": input,
            "target": target,
            "prediction": prediction,
            "domain": domain,
            "correct": is_correct,
        })

        time.sleep(0.2)
    
    result_file = Path(f"evaluation_{strategy}.json")
    with result_file.open("w") as f:
        json.dump(results, f, indent=2)
    
    print("Evaluation for strategy:", strategy)

    correct_answers = 0
    total_questions = 0

    for domain in total_per_domain:
        correct = correct_per_domain[domain]
        total = total_per_domain[domain]
        correct_answers += correct
        total_questions += total
        accuracy = 100 * (correct/total) if total > 0 else 0.0
        print(f"domain: {domain} ({correct}/{total}) accuracy: {accuracy:.2f}%")
    
    overall_accuracy = 100 * (correct_answers/total_questions)
    print(f"Overall accuracy: {overall_accuracy:.2f}% ({correct_answers}/{total_questions})")

    return results

def main():
    ### You can change the path to dev set file as needed.
    dev_data_path = Path("sub_dev_set.json")
    dev_data = load_dev_data(dev_data_path)

    ### You can change the strategy value here for testing.
    ### Supported strategies: baseline, self_consistency, self_refine, CoT
    evaluate(dev_data, strategy="CoT")

if __name__ == "__main__":
    main()
