import re
from pathlib import Path

RAW_DIR = Path("raw/xhosa")
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CORPUS_PATH = OUTPUT_DIR / "corpus.txt"

def clean_text(text: str) -> str:
    text = re.sub(r"[^a-zA-Z0-9áéíóúüñç\s\.,?!]", "", text)

    text = re.sub(r"([.,?!])", r" \1 ", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text

all_lines = []
for file in RAW_DIR.glob("*.xh.txt"):
    print(f"Processing {file}...")
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = clean_text(line)
            if line: 
                all_lines.append(line)

with open(CORPUS_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(all_lines))

print(f"Corpus built with {len(all_lines)} lines at {CORPUS_PATH}")
