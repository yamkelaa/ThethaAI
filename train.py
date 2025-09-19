import pickle
from pathlib import Path
from collections import defaultdict

CORPUS_PATH = Path("data/processed/corpus.txt")
MODEL_PATH = Path("src/model/ngram_model.pkl")

# Load corpus
input_to_response = {}
all_responses = []

with open(CORPUS_PATH, "r", encoding="utf-8") as f:
    for line in f:
        if "|" not in line:
            continue
        user_input, response = line.strip().split("|", 1)
        input_to_response[user_input.lower()] = response
        all_responses.append(response)

# Build word-level n-gram model on responses
def build_ngram_model(corpus_lines, n=2):
    model = defaultdict(list)
    for line in corpus_lines:
        words = ["~"] * (n - 1) + line.split() + ["~"]
        for i in range(len(words) - n + 1):
            key = tuple(words[i:i + n - 1])
            next_word = words[i + n - 1]
            model[key].append(next_word)
    return dict(model)

ngram_model = build_ngram_model(all_responses, n=2)

# Save everything
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump({"input_to_response": input_to_response, "ngram_model": ngram_model}, f)

print(f"✅ Model trained and saved at {MODEL_PATH}")
