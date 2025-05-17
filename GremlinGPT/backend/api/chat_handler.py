from flask import request, jsonify
from backend.interface import commands
from nlp_engine.tokenizer import tokenize
from nlp_engine.transformer_core import encode
from agent_core.task_queue import enqueue_task
from memory.vector_store.embedder import package_embedding

def chat():
    data = request.get_json()
    user_input = data.get("text", "")

    tokens = tokenize(user_input)
    vector = encode(user_input)

    task = commands.parse_command(user_input)
    result = commands.execute_command(task)

    package_embedding(text=user_input, vector=vector, meta={"from": "chat"})

    return jsonify({
        "response": f"Command interpreted as: {task['type']}",
        "tokens": tokens,
        "result": result
    })

