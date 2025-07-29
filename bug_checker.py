# bug_checker.py
import requests
from concurrent.futures import ThreadPoolExecutor
import time

# Baca daftar bug dari file eksternal
def load_bug_list(filename="list-bug.txt"):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"\u274c File '{filename}' tidak ditemukan.")
        return []

def check_bug(host):
    url = f"https://{host}"
    try:
        response = requests.get(url, timeout=5)
        code = response.status_code
        if code in [101]:
            return f"\u2728 {host} — Switching Protocols (101)"
        elif code in [200, 301, 302]:
            return f"\u2705 {host} — LIVE ({code})"
        elif code == 403:
            return f"⚠️ {host} — Terlarang ({code})"
        else:
            return f"\u274c {host} — Gagal ({code})"
    except requests.exceptions.RequestException:
        return f"\u274c {host} — Timeout / Tidak Terhubung"

def check_bug_with_payload(host):
    url = f"https://{host}"
    headers = {
        "Host": host,
        "X-Online-Host": host,
        "User-Agent": "Mozilla/5.0",
        "Connection": "Upgrade"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        code = response.status_code
        if code == 101:
            return f"\u2728 {host} — Switching Protocols via payload (101)"
        elif code in [200, 301, 302]:
            return f"\u2705 {host} — LIVE via payload ({code})"
        elif code == 403:
            return f"⚠️ {host} — Terlarang via payload ({code})"
        else:
            return f"\u274c {host} — Gagal via payload ({code})"
    except requests.exceptions.RequestException:
        return f"\u274c {host} — Timeout via payload"

def main():
    bug_list = load_bug_list()
    if not bug_list:
        return

    print("=== CEK BUG HOST MULTI ===")
    print("Mode: 1) Normal  2) Pakai Payload")
    mode = input("Pilih mode (1/2): ").strip()

    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        if mode == "2":
            results = executor.map(check_bug_with_payload, bug_list)
        else:
            results = executor.map(check_bug, bug_list)

    for result in results:
        print(result)

    print(f"\nSelesai dalam {round(time.time() - start, 2)} detik.")

if __name__ == "__main__":
    main()
