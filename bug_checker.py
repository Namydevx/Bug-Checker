import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Baca daftar bug dari file eksternal
def load_bug_list(filename="list-bug.txt"):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"❌ File '{filename}' tidak ditemukan.")
        return []

def check_bug(host):
    url = f"https://{host}"
    try:
        response = requests.get(url, timeout=5)
        code = response.status_code
        if code in [200, 301, 302]:
            return f"✅ {host} — LIVE ({code})"
        elif code == 403:
            return f"⚠️ {host} — Terlarang ({code})"
        else:
            return f"❌ {host} — Gagal ({code})"
    except requests.exceptions.RequestException:
        return f"❌ {host} — Timeout / Tidak Terhubung"

def main():
    bug_list = load_bug_list()
    if not bug_list:
        return

    print("=== CEK BUG HOST MULTI ===\n")
    start = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check_bug, bug_list)
    
    for result in results:
        print(result)

    print(f"\nSelesai dalam {round(time.time() - start, 2)} detik.")

if __name__ == "__main__":
    main()
