from fastapi import FastAPI, UploadFile, File, Request
from pydantic import BaseModel
from nlp_engine import (
    parser, tokenizer, pos_tagger, semantic_score, diff_engine, transformer_core, mini_attention
)
import uvicorn

app = FastAPI(title="GremlinGPT NLP Engine API")

class TextPair(BaseModel):
    text_a: str
    text_b: str

class TextInput(BaseModel):
    text: str

class DiffInput(BaseModel):
    old: str
    new: str
    debug: bool = False

@app.post("/tokenize")
def tokenize(req: TextInput):
    return {"tokens": tokenizer.tokenize(req.text)}

@app.post("/pos_tags")
def pos_tags(req: TextInput):
    return {"pos_tags": pos_tagger.get_pos_tags(req.text)}

@app.post("/semantic_similarity")
def semantic_similarity(req: TextPair):
    score = semantic_score.semantic_similarity(req.text_a, req.text_b)
    return {"semantic_similarity": score}

@app.post("/most_similar")
def most_similar(req: TextInput, candidates: list[str]):
    match, score = semantic_score.most_similar(req.text, candidates)
    return {"most_similar": match, "score": score}

@app.post("/parse")
def parse(req: TextInput):
    return parser.parse_nlp(req.text)

@app.post("/diff_texts")
def diff_texts(req: DiffInput):
    return diff_engine.diff_texts(req.old, req.new, debug=req.debug)

@app.post("/diff_files")
def diff_files(file_a: UploadFile = File(...), file_b: UploadFile = File(...)):
    content_a = file_a.file.read().decode("utf-8")
    content_b = file_b.file.read().decode("utf-8")
    return diff_engine.diff_texts(content_a, content_b)

@app.post("/encode_text")
def encode(req: TextInput):
    vec = transformer_core.encode_text(req.text)
    return {"embedding": vec.tolist()}

# Optional: For model testing
@app.post("/attention_forward")
def attention_forward(embed_dim: int, num_heads: int, data: list[list[float]]):
    import numpy as np
    arr = np.array(data)
    attn = mini_attention.MiniMultiHeadAttention(embed_dim, num_heads)
    out, wts = attn.forward(arr)
    return {"output": out.tolist(), "weights": wts.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
