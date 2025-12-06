# Inference time reasoning methods

## TL;DR

Implemented 3 inference time reasoning methods:
    - self consistency multiple CoTs and majority voting.

    - self refine - 3 llm calls (initial answer, critique, refined answer)

    - Chain of Thoughts - 2 llm calls (thinking, final answer)

- To run the test:
    - Go to "generate_answer_template.py"

    - Select the value of strategy to put inside 
    ```python
    agent = Agent(strategy="your_strategy_value")
    ```
    
    - choose the values among ("self_consistency", "self_refine", "CoT")

    - Run "generate_answer_template.py"



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

- I had number of samples (n) = 7, and temperature = 0.7 for answer diversity. So for each question, it calls llm 7 times (7000 calls).

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

## Commit 7: Implemented Self refine method

- Self refine method contains 3 steps:
- - Initial answer by model
- - Give the answer to the model again and ask to critique, and give feedback for improvements
- - Give the critique, question, and initial answer, ask the model to refine the answer and output final answer.

- This time, I reduced the testing to few examples from all the domain in the dev set. Made sub_dev_set.json and added examples from the given dev set, for faster run times.

As I reduced the size of examples, it gave almost 0 accuracy since I changed the system prompt for refinement step that changed the formatting. 

I tried with various prompts afterwards but finally got less improvements:
NOTE: the number of questions reduced per domain.
```bash
Evaluation started with strategy: self_refine
Evaluation for strategy: self_refine
domain: math (0/14) accuracy: 0.00%
domain: coding (0/11) accuracy: 0.00%
domain: future_prediction (0/4) accuracy: 0.00%
domain: planning (0/17) accuracy: 0.00%
domain: common_sense (3/29) accuracy: 10.34%
Overall accuracy: 4.00% (3/75)
```

## Commit 8: Implemented Chain of Thought method as strategy 3

- I wanted to experiment with a simpler yet effective method.
- In this method, I call the llm two times.
    - First to get thought process (think step by step but not give the final answer yet)
    - Based on the thought process and question, asked llm to give final answer.

Surprisingly for small amount of dev data, it did better than self refine for common_sense.

result:
```bash
Evaluation started with strategy: CoT
Evaluation for strategy: CoT
domain: math (0/14) accuracy: 0.00%
domain: coding (0/11) accuracy: 0.00%
domain: future_prediction (0/4) accuracy: 0.00%
domain: planning (0/17) accuracy: 0.00%
domain: common_sense (11/29) accuracy: 37.93%
Overall accuracy: 14.67% (11/75)
```
Again, some responses still matches the output but just not in the right format.

## Commit 9: Final Test:

### How to run:

In the file 'generate_answer_template.py', check the 
```python
build_answer()
```
function. 

- In the build_answer() function, I have declared and initialized Agent with strategy = "CoT", which represents Chain of Thoughts strategy. You can change the strategy value to other following strategies:
```bash
"self_consistency"
"self_refine"
"CoT"
```

- Run generate_answer_template.py

### Output I got:

- Ran for almost 8 hours (4:45 PM - 12:45 AM)

Terminal output:
```bash
Processed 100 questions.
Processed 200 questions.
Processed 300 questions.
Processed 400 questions.
Processed 500 questions.
Processed 600 questions.
Processed 700 questions.
Processed 800 questions.
Processed 900 questions.
Processed 1000 questions.
Processed 1100 questions.
Processed 1200 questions.
Processed 1300 questions.
Processed 1400 questions.
Processed 1500 questions.
Processed 1600 questions.
Processed 1700 questions.
Processed 1800 questions.
Processed 1900 questions.
Processed 2000 questions.
Processed 2100 questions.
Processed 2200 questions.
Processed 2300 questions.
Processed 2400 questions.
Processed 2500 questions.
Processed 2600 questions.
Processed 2700 questions.
Processed 2800 questions.
Processed 2900 questions.
Processed 3000 questions.
Processed 3100 questions.
Processed 3200 questions.
Processed 3300 questions.
Processed 3400 questions.
Processed 3500 questions.
Processed 3600 questions.
Processed 3700 questions.
Processed 3800 questions.
Processed 3900 questions.
Processed 4000 questions.
Processed 4100 questions.
Processed 4200 questions.
Processed 4300 questions.
Processed 4400 questions.
Processed 4500 questions.
Processed 4600 questions.
Processed 4700 questions.
Processed 4800 questions.
Processed 4900 questions.
Processed 5000 questions.
Processed 5100 questions.
Processed 5200 questions.
Processed 5300 questions.
Processed 5400 questions.
Processed 5500 questions.
Processed 5600 questions.
Processed 5700 questions.
Processed 5800 questions.
Processed 5900 questions.
Processed 6000 questions.
Processed 6100 questions.
Processed 6200 questions.
Wrote 6208 answers to cse_476_final_project_answers.json and validated format successfully.
```

- Updated the cse_476_final_project_answers.json with the answers

## output files:

- I have implemented to push all the model prediction, output for comparison for each strategy.
- Baseline (without any modification to prompt, or any methods) - evaluation_baseline.json
- self consistency - evaluation_self_consistency.json
- self refine - evaluation_self_refine.json
- Chain of Thoughts - evaluation_CoT.json

- Ran the final test and have answers for test data in
cse_476_final_project_answers.json

## References:

Inference-Time Computations for LLM Reasoning and Planning: A Benchmark and Insights - https://arxiv.org/abs/2502.12521

Prompting tehniques - https://www.promptingguide.ai/techniques