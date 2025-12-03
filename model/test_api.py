from .api import call_model_chat_completions

demo_prompt = "What is 17 + 28? Answer with just the number."
result = call_model_chat_completions(demo_prompt)
print("OK:", result["ok"], "HTTP:", result["status"])
print("MODEL SAYS:", (result["text"] or "").strip())

# Optional: Inspect rate-limit headers if your provider exposes them
for k in ["x-ratelimit-remaining-requests", "x-ratelimit-limit-requests", "x-request-id"]:
    if k in result["headers"]:
        print(f"{k}: {result['headers'][k]}")