import os
import openai
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_python_files():
    tracked_files = []
    for root, _, files in os.walk("."):
        for f in files:
            if f.endswith(".py") and ".venv" not in root and "site-packages" not in root:
                tracked_files.append(os.path.join(root, f))
    return tracked_files

def build_prompt(code):
    return f"""
You're a senior Python reviewer AI. Analyze the following code for:
- bugs
- insecure logic
- poor practices
- non-PEP8 formatting

Then respond with JSON containing:
- `filename`
- `issues`: a list of found problems
- `suggestions`: human-readable recommended fixes

Code:
\"\"\"
{code}
\"\"\"
"""

def run_review():
    files = get_python_files()
    results = []

    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()

        prompt = build_prompt(code)
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python code reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        result = {
            "filename": path,
            "review": response['choices'][0]['message']['content']
        }
        results.append(result)

    with open("ai-review.json", "w") as out:
        json.dump(results, out, indent=4)
    print("[smart_review_agent] Completed review. Results saved to ai-review.json.")

if __name__ == "__main__":
    run_review()
