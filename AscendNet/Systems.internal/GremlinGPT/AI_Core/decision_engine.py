import re
import openai
from memory import vector_store, planning_memory

def make_decision(prompt):
    # Retrieve relevant context from vector store
    context = vector_store.retrieve(prompt)

    # Combine prompt with context
    full_prompt = f"{context}\n\n{prompt}"

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": full_prompt}]
    )

    decision = response['choices'][0]['message']['content']
    planning_memory.store(prompt, decision)
    return decision

def decision_node(task_text: str, context: str = "") -> dict:
    """Very dumb but functional decision logic based on keywords. Replace this with LLM-based planning later."""
    task = task_text.lower()

    # Decision logic: this is primitive — just matching keywords
    if "scrape" in task:
        return {
            "type": "tool",
            "name": "scrape_web",
            "params": {"url": extract_url(task)}
        }
    elif "api" in task or "price" in task:
        return {
            "type": "tool",
            "name": "query_api",
            "params": {"endpoint": extract_url(task)}
        }
    elif "buy crypto" in task or "regret" in task:
        return {
            "type": "tool",
            "name": "buy_crypto",
            "params": {"amount": extract_amount(task)}
        }
    else:
        return {
            "type": "code",
            "code": generate_code_prompt(task, context)
        }

def extract_url(text):
    match = re.search(r'(https?://\S+)', text)
    return match.group(1) if match else "https://example.com"

def extract_amount(text):
    match = re.search(r'(\d+)', text)
    return float(match.group(1)) if match else 10.0

def generate_code_prompt(task, context):
    return f"# Context: {context}\n# Task: {task}\nWrite a Python function to solve this."
