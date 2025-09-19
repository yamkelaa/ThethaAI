import random
from collections import defaultdict

def build_ngram_model(conversations, n=2):
    """
    Builds a word-level n-gram model from input-response pairs.
    :param conversations: list of (input_line, response_line) tuples
    :param n: n-gram size (number of words)
    :return: dict mapping (n-1)-grams -> possible next words
    """
    model = defaultdict(list)
    
    for _, response in conversations:
        words = response.strip().split()
        if not words:
            continue
        padded = ["~"] * (n - 1) + words + ["~"]
        for i in range(len(padded) - n + 1):
            key = tuple(padded[i:i + n - 1])
            next_word = padded[i + n - 1]
            model[key].append(next_word)
    
    return dict(model)

def generate_text(model, start_words=None, n=2, max_words=20):
    """
    Generate text from a word-level n-gram model.
    :param model: n-gram dict
    :param start_words: list of starting words (optional)
    :param n: n-gram size
    :param max_words: maximum number of words to generate
    """
    if start_words is None:
        start_words = ["~"] * (n - 1)
    else:
        start_words = ["~"] * max(0, n - 1 - len(start_words)) + start_words[-(n-1):]

    result = list(start_words)
    
    for _ in range(max_words):
        key = tuple(result[-(n - 1):])
        possible = model.get(key, ["~"])
        next_word = random.choice(possible)
        if next_word == "~":
            break
        result.append(next_word)
    
    return " ".join(result[(n - 1):])