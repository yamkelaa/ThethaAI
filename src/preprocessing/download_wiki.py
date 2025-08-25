import os
import requests

def download_xhosa_wiki():
    url = "https://dumps.wikimedia.org/xhwiki/latest/xhwiki-latest-pages-articles.xml.bz2"
    raw_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
    os.makedirs(raw_dir, exist_ok=True)

    file_path = os.path.join(raw_dir, "xhwiki-latest-pages-articles.xml.bz2")

    if os.path.exists(file_path):
        print("File already downloaded:", file_path)
        return file_path

    print("Downloading isiXhosa Wikipedia dump...")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(file_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print("Download complete:", file_path)
    return file_path

if __name__ == "__main__":
    download_xhosa_wiki()
