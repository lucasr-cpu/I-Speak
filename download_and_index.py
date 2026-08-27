import os
import json
import urllib.request
import time

API_METADATA_URL = "https://api.arasaac.org/v1/pictograms/all/en"
IMAGE_BASE_URL = "https://api.arasaac.org/v1/pictograms/"
SYMBOLS_DIR = "./symbols"
LIBRARY_FILE = "symbols-library.json"

def setup_environment():
    if not os.path.exists(SYMBOLS_DIR):
        os.makedirs(SYMBOLS_DIR)
        print(f"[+] Created directory: {SYMBOLS_DIR}")

def fetch_metadata():
    print("[*] Fetching pictogram metadata from ARASAAC API...")
    req = urllib.request.Request(API_METADATA_URL, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            print(f"[+] Retrieved metadata for {len(data)} pictograms.")
            return data
    except Exception as e:
        print(f"[-] Error fetching metadata index: {e}")
        return []

def download_and_index():
    setup_environment()
    pictograms = fetch_metadata()
    if not pictograms:
        print("[-] Pipeline aborted: Missing metadata.")
        return

    symbol_index = {}
    total = len(pictograms)
    print(f"[*] Downloading and indexing {total} pictograms...")

    for idx, pic in enumerate(pictograms, start=1):
        pic_id = pic.get("_id")
        keywords = [k.get("keyword").lower() for k in pic.get("keywords", []) if k.get("keyword")]
        
        if not pic_id:
            continue

        filename = f"{pic_id}.png"
        filepath = os.path.join(SYMBOLS_DIR, filename)
        
        if not os.path.exists(filepath):
            img_url = f"{IMAGE_BASE_URL}{pic_id}?download=false"
            try:
                img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(img_req) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
                time.sleep(0.01)  # Safeguard rate limit
            except Exception as e:
                print(f"[-] Failed ID {pic_id}: {e}")
                continue

        local_rel_path = f"symbols/{filename}"
        symbol_index[str(pic_id)] = local_rel_path
        
        for kw in keywords:
            if kw not in symbol_index:
                symbol_index[kw] = local_rel_path

        if idx % 500 == 0 or idx == total:
            print(f"[{idx}/{total}] Processed... ({int((idx/total)*100)}%)")

    with open(LIBRARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(symbol_index, f, indent=2)
    
    print(f"[+] Complete! Master index saved to {LIBRARY_FILE}")

if __name__ == "__main__":
    download_and_index()