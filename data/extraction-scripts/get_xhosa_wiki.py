import re
import requests
import bz2
import xml.etree.ElementTree as ET
from pathlib import Path

# ------------------------------
# 1. Download Wikipedia Dump
# ------------------------------
dump_url = "https://dumps.wikimedia.org/xhwiki/latest/xhwiki-latest-pages-articles.xml.bz2"
raw_folder = Path("../data/raw")
raw_folder.mkdir(parents=True, exist_ok=True)

dump_path = raw_folder / "xhwiki-latest-pages-articles.xml.bz2"
xml_path = raw_folder / "xhwiki-latest-pages-articles.xml"

if not dump_path.exists():
    print("📥 Downloading isiXhosa Wikipedia Dump...")
    r = requests.get(dump_url, stream=True)
    with open(dump_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024*1024):
            if chunk:
                f.write(chunk)
    print("✅ Download complete.")

# ------------------------------
# 2. Decompress BZ2 to XML
# ------------------------------
if not xml_path.exists():
    print("📂 Decompressing...")
    with bz2.open(dump_path, "rb") as f_in:
        with open(xml_path, "wb") as f_out:
            f_out.write(f_in.read())
    print("✅ Decompression complete.")

# ------------------------------
# 3. Extract Plain Text
# ------------------------------
def clean_wiki_markup(text: str) -> str:
    """Remove Wikipedia markup and XML tags."""
    text = re.sub(r"<.*?>", "", text)  # XML tags
    text = re.sub(r"\{\{.*?\}\}", "", text)  # templates
    text = re.sub(r"\[\[(File|Image):.*?\]\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[\[(.*?)\|(.*?)\]\]", r"\2", text)  # keep visible link text
    text = re.sub(r"\[\[(.*?)\]\]", r"\1", text)
    text = re.sub(r"={2,}.*?={2,}", "", text)  # headings
    text = re.sub(r"\n+", "\n", text)
    return text.strip()

def extract_wiki_text(xml_file, output_file):
    print("🔎 Extracting plain text from XML (this may take a while)...")
    with open(output_file, "w", encoding="utf-8") as out:
        for event, elem in ET.iterparse(xml_file, events=("end",)):
            if elem.tag.endswith("text"):
                raw_text = elem.text or ""
                clean_text = clean_wiki_markup(raw_text)
                if clean_text.strip():
                    out.write(clean_text + "\n")
                elem.clear()  # free memory
    print(f"✅ Extraction complete → {output_file}")

output_file = raw_folder / "isiXhosa_wikipedia.txt"
if not output_file.exists():
    extract_wiki_text(xml_path, output_file)
