import random
from collections import defaultdict

def build_ngram_model(corpus_lines, n=3):
    """
    Builds a character-level n-gram model.
    :param corpus_lines: list of strings
    :param n: n-gram size
    :return: dict mapping (n-1)-grams -> possible next chars
    """
    model = defaultdict(list)

    for line in corpus_lines:
        padded_line = "~" * (n - 1) + line + "~"  # start/end markers
        for i in range(len(padded_line) - n + 1):
            key = padded_line[i:i + n - 1]
            next_char = padded_line[i + n - 1]
            model[key].append(next_char)

    return dict(model)


def generate_text(model, length=100, n=3):
    """
    Generate text from an n-gram model.
    :param model: n-gram dict
    :param length: number of characters to generate
    :param n: n-gram size
    """
    start = "~" * (n - 1)
    result = start

    for _ in range(length):
        key = result[-(n - 1):]
        possible = model.get(key, [" "])
        next_char = random.choice(possible)
        if next_char == "~":
            break
        result += next_char

    return result[(n - 1):]
