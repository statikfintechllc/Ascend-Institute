# run_llama.py

import os
import time
import uuid
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Literal, Optional
from llama_cpp import Llama
import uvicorn

# --- Environment Setup ---
os.environ["LLAMA_CPP_FORCE_CUDA"] = "1"
os.environ["GGML_CUDA_FORCE_MMQ"] = "1"
os.environ["GGML_CUDA_PEER_ACCESS"] = "0"  # PHB → disabled to avoid false expectations

# --- Model Configuration ---
MODEL_PATH = "/home/statiksmoke8/AscendNet/godcore/models/Mistral-13B-Instruct/mistral-13b-instruct-v0.1.Q5_K_M.gguf"
TENSOR_SPLIT = "20,20"  # Explicit per-GPU split

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,
    n_gpu_layers=35,
    main_gpu=0,
    TENSOR_SPLIT=[
        0.5,
        0.5,
    ],  # or manually [0.48, 0.52] if one GPU has slightly more VRAM
    n_threads=24,
    use_mmap=True,
    use_mlock=False,
    verbose=True,
)

# --- FastAPI Setup ---
app = FastAPI()


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    top_p: Optional[float] = 0.9
    max_tokens: Optional[int] = 16384  # Cap for safety on 12GB cards
    stop: Optional[List[str]] = None


@app.get("/")
def root():
    return {
        "message": "Mistral LLaMA API is live. Use POST /v1/chat/completions to interact."
    }


@app.post("/v1/chat/completions")
def chat_completion(request: ChatRequest):
    prompt = "".join(
        [
            f"{msg.role.capitalize()}: {msg.content.strip()}\n"
            for msg in request.messages
        ]
    )
    prompt += "Assistant:"

    try:
        output = llm(
            prompt=prompt,
            temperature=request.temperature,
            top_p=request.top_p,
            max_tokens=request.max_tokens,
            stop=request.stop or ["</s>", "User:", "Assistant:"],
        )
    except Exception as e:
        return {"error": "InferenceFailure", "detail": str(e)}

    return {
        "id": f"chatcmpl-{uuid.uuid4().hex[:12]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": request.model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": output["choices"][0]["text"].strip(),
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": output.get("prompt_tokens", 0),
            "completion_tokens": output.get("completion_tokens", 0),
            "total_tokens": output.get("prompt_tokens", 0)
            + output.get("completion_tokens", 0),
        },
    }


if __name__ == "__main__":
    print("🚀 Devin-compatible API ready on http://localhost:8000")
    uvicorn.run("run_llama:app", host="0.0.0.0", port=8000)
