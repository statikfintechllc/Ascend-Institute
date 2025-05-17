from nlp_engine.tokenizer import tokenize
from nlp_engine.pos_tagger import get_pos_tags
from nlp_engine.transformer_core import encode
from nlp_engine.diff_engine import vector_diff

def test_tokenizer():
    tokens = tokenize("Run GremlinGPT on boot.")
    assert "Run" in tokens

def test_pos():
    tags = get_pos_tags("Run the agent task.")
    assert any(tag[1] for tag in tags)

def test_encode_and_diff():
    vec1 = encode("Test vector one.")
    vec2 = encode("Test vector two.")
    score = vector_diff("Test vector one.", "Test vector two.")
    assert 0 <= score <= 1

