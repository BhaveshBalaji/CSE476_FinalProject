# Inference time reasoning methods

## Steps I took:

- I referred to some papers related to inference time reasoning methods, to understand which method is suitable for what type of domain.
- My first intuition is to develop an evaluator that can test the model's accuracy on different domains. 
- So, I have developed an evaluator with functions from tutorial.py for normalization and grade, plus I want to generate an output json file to see if the model actually produces the expected format.
- First, I want to test the model's performance without any methods implemented to understand on what domains it is strong, and weak.

My first execution of evaluate.py: 
```bash
Evaluation started with strategy: baseline
Evaluation for strategy: baseline
domain: math (5/300) accuracy: 1.67%
domain: coding (0/100) accuracy: 0.00%
domain: future_prediction (0/100) accuracy: 0.00%
domain: planning (0/100) accuracy: 0.00%
domain: common_sense (42/400) accuracy: 10.50%
Overall accuracy: 4.70% (47/1000)
```
I saw the outputs and it has "yes.", "no." instead of true or false. So, I need to refine my evaluator and system prompt.


## Commit 4: Refined evaluator.py

- I have added implementation for removing articles because I saw some answers are correct but just have one article that makes it not countable for accuracy. 
- Added synonyms for true/false questions (yes-true, no-false)
- Modified system prompt to make it strictly adhere to output format either specified in the user prompt or just give the final answer without any reasoning steps.
- Even more common_sense questions would have matched for multiple choice questions if the model didn't add the choice number and just the answer.

result:
```bash
Evaluation started with strategy: baseline
Evaluation for strategy: baseline
domain: math (9/300) accuracy: 3.00%
domain: coding (0/100) accuracy: 0.00%
domain: future_prediction (0/100) accuracy: 0.00%
domain: planning (0/100) accuracy: 0.00%
domain: common_sense (118/400) accuracy: 29.50%
Overall accuracy: 12.70% (127/1000)
```

- Showed improvement on common_sense questions and very little on math. Coding, future_prediction, and planning are still not improved.
- For math, some answers are right but the target output have reasons, and for some items where the target output is just one number, the model responded with explanation even when the system prompt says to strictly give final answer for numeric problems.

## Commit 5: Added self consistency inference time reasoning method

- The first method I developed is self consistency method which I referred from course lecture notes and prompting guide reference (given below under references).

- In this method, I have a list of answers that I will get from multiple Chain of Thoughts, and get the most common answer (majority voting).

- I had number of samples (n) = 7. So for each question, it calls llm 7 times (7000 calls).

result:
```bash
Evaluation started with strategy: self_consistency
Evaluation for strategy: self_consistency
domain: math (11/300) accuracy: 3.67%
domain: coding (0/100) accuracy: 0.00%
domain: future_prediction (0/100) accuracy: 0.00%
domain: planning (0/100) accuracy: 0.00%
domain: common_sense (121/400) accuracy: 30.25%
Overall accuracy: 13.20% (132/1000)
```

- It didn't show much difference on the evaluate.py output but as I went over the output json file (evaluation_self_consistency.json), I can see that it has given positive answers for planning, and a few future prediction questions, but the output format didn't match with the target output causing them to show up as a fail.


## References:

Inference-Time Computations for LLM Reasoning and Planning: A Benchmark and Insights - https://arxiv.org/abs/2502.12521

Prompting tehniques - https://www.promptingguide.ai/techniques