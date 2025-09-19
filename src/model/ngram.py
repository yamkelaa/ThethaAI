import random
from collections import defaultdict

def build_ngram_model(corpus_lines, n=3):
    """
    Builds a word-level n-gram model.
    :param corpus_lines: list of strings
    :param n: n-gram size
    :return: dict mapping (n-1)-grams -> possible next words
    """
    model = defaultdict(list)

    for line in corpus_lines:
        words = line.strip().split()
        if len(words) < n:
            continue
        padded = ["<s>"] * (n - 1) + words + ["</s>"]
        for i in range(len(padded) - n + 1):
            key = tuple(padded[i:i + n - 1])
            next_word = padded[i + n - 1]
            model[key].append(next_word)

    return dict(model)


def generate_text(model, n=3, max_words=30, stop_at_punct=True):
    """
    Generate text from a word-level n-gram model.
    :param model: n-gram dict
    :param n: n-gram size
    :param max_words: maximum number of words
    """
    start = ("<s>",) * (n - 1)
    result = list(start)

    for _ in range(max_words):
        key = tuple(result[-(n - 1):])
        possible = model.get(key, ["</s>"])
        next_word = random.choice(possible)

        if next_word == "</s>":
            break

        result.append(next_word)

        if stop_at_punct and next_word.endswith((".", "?", "!")):
            break

    return " ".join(result[(n - 1):])
