from nlp_engine.tokenizer import tokenize
from nlp_engine.pos_tagger import get_pos_tags

def parse_nlp(text):
    return {
        "tokens": tokenize(text),
        "pos": get_pos_tags(text)
    }

