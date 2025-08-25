import os
import bz2
import re

RAW_DATA_PATH = os.path.join("data", "raw", "xhwiki-latest-pages-articles.xml.bz2")
OUTPUT_PATH = os.path.join("data", "processed", "xhwiki_clean.txt")

def strip_tags(text):
    """Remove XML/HTML tags and extra markup."""
    text = re.sub(r"<[^>]+>", " ", text)       
    text = re.sub(r"\{\{.*?\}\}", " ", text)   
    text = re.sub(r"\[\[.*?\]\]", " ", text)   
    text = re.sub(r"\s+", " ", text)           
    return text.strip()

def preprocess_wiki():
    print(f"📂 Reading from {RAW_DATA_PATH}")
    with bz2.open(RAW_DATA_PATH, "rt", encoding="utf-8") as f_in, \
         open(OUTPUT_PATH, "w", encoding="utf-8") as f_out:
        for i, line in enumerate(f_in):
            clean_line = strip_tags(line)
            if clean_line:
                f_out.write(clean_line + "\n")
            if i % 100000 == 0:   # progress checkpoint
                print(f"Processed {i} lines...")

    print(f"🎉 Preprocessing complete. Output saved at: {OUTPUT_PATH}")

if __name__ == "__main__":
    preprocess_wiki()
