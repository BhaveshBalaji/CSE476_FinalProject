import json
import time
import re
from agent import Agent
from pathlib import Path
from typing import Any, Dict, List

"""
Intuition: I created this file to evaluate the accuracy of model with different inference
time methods or strategies starting with baseline (no method used, just testing
how good the model is).
"""
# Erase punctuation
ARTICLES = {"a", "an", "the"}

def normalize_text(s: str) -> str:
    # handle boolean values to pass through questions in common_sense domain (boolean to string)
    if isinstance(s, bool):
        s = "true" if s else "false"

    s = (s or "").strip().lower()

    # Remove surrounding punctuation and extra whitespace
    s = re.sub(r"[^\w\s\-']", " ", s)
    s = re.sub(r"\s+", " ", s).strip()

    # Remove articles as I saw some answers are not accurate just because of extra articles.
    tokens = [t for t in s.split() if t not in ARTICLES]

    # Map common synonyms used in these tests
    synonyms = {
        "unchanged": "stay the same",
        "no change": "stay the same",
        "same": "stay the same",
        "second place": "second",
        "2nd": "second",
        "first place": "first",
        "third place": "third",
        
        # true or false synonyms to see if it improves common_sense accuracy
        "true": "true",
        "false": "false",
        "yes": "true",
        "no": "false",
    }
    tokens = [synonyms.get(t, t) for t in tokens]

    return " ".join(tokens)

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
    dev_data_path = Path("cse476_final_project_dev_data.json")
    dev_data = load_dev_data(dev_data_path)
    evaluate(dev_data, strategy="baseline")

if __name__ == "__main__":
    main()
