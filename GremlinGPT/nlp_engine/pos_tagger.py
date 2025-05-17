import nltk
from nltk import pos_tag, word_tokenize
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def get_pos_tags(text):
    tokens = word_tokenize(text)
    return pos_tag(tokens)

