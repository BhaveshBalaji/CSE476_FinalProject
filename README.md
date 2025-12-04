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


## References:

Inference-Time Computations for LLM Reasoning and Planning: A Benchmark and Insights - https://arxiv.org/abs/2502.12521

Prompting tehniques - https://www.promptingguide.ai/techniques