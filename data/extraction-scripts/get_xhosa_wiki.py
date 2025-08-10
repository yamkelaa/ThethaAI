import re
import requests
import bz2

#downloading the latest isiXhosa Wikipedia Dump
#storing them under my raw data folder
dump_url = "https://dumps.wikimedia.org/xhwiki/latest/xhwiki-latest-pages-articles.xml.bz2"
dump_path = "../raw/xhwiki-latest-pages-articles.xml.bz"

print("Busy downloading the isiXhosa Dump")
r = requests.get(dump_url, stream=True)
with open(dump_path, "wb") as f:
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            f.write(chunk)
print("Download is now complete")

xml_path = dump_path.replace(".bz2", "")
print("Decompressing...")
with bz2.open(dump_path, "rb") as f_in:
    with open(xml_path, "wb") as f_out:
        f_out.write(f_in.read())
print("✅ Decompression complete.")

def extract_wiki_text(xml_file, output_file):
    print("Extracting plain text from XML...")
    with open(xml_file, "r", encoding="utf-8") as f:
        text = f.read()
     # Remove XML tags
    clean = re.sub(r"<.*?>", "", text)
    # Remove wiki templates {{...}}
    clean = re.sub(r"\{\{.*?\}\}", "", clean)
    # Remove file/image links [[File:...]] or [[Image:...]]
    clean = re.sub(r"\[\[(File|Image):.*?\]\]", "", clean, flags=re.IGNORECASE)
    # Remove other links but keep the visible text
    clean = re.sub(r"\[\[(.*?)\|(.*?)\]\]", r"\2", clean)
    clean = re.sub(r"\[\[(.*?)\]\]", r"\1", clean)
    # Remove extra whitespace
    clean = re.sub(r"\n+", "\n", clean).strip()

    with open(output_file, "w", encoding="utf-8") as out:
        out.write(clean)
    print("Extraction completed")

output_file = "../raw/isiXhosa_wikipedia.txt"
extract_wiki_text(xml_path, output_file)