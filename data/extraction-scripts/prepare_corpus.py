import re
from pathlib import Path

# Adjust relative path to where you run the script
RAW_DIR = Path(__file__).parent / "../../raw/xhosa"  
OUTPUT_DIR = Path(__file__).parent / "../../data/processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CORPUS_PATH = OUTPUT_DIR / "corpus.txt"

def clean_text(text: str) -> str:
    # Keep letters, numbers, basic punctuation
    text = re.sub(r"[^a-zA-Z0-9\s.,?!]", "", text)
    # Add spaces around punctuation for tokenization
    text = re.sub(r"([.,?!])", r" \1 ", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text

all_lines = []
for file in RAW_DIR.glob("*-xh.txt"):  # matches your files
    print(f"Processing {file}...")
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = clean_text(line)
            if line:
                all_lines.append(line)

# Save processed corpus
with open(CORPUS_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(all_lines))

print(f"✅ Corpus built with {len(all_lines)} lines at {CORPUS_PATH}")
