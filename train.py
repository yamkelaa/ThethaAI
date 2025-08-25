import pickle
from pathlib import Path
from src.model.ngram import build_ngram_model

CORPUS_PATH = Path("data/processed/xhwiki_clean.txt")
MODEL_PATH = Path("data/processed/ngram_model.pkl")

# Load corpus
with open(CORPUS_PATH, "r", encoding="utf-8") as f:
    corpus_lines = [line.strip() for line in f if line.strip()]

# Train model
print("Training n-gram model...")
ngram_model = build_ngram_model(corpus_lines, n=3)

# Save model
MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(MODEL_PATH, "wb") as f:
    pickle.dump(ngram_model, f)

print(f"Model trained and saved at {MODEL_PATH}")
