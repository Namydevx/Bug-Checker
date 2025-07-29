import requests
from concurrent.futures import ThreadPoolExecutor
import time
import socket
import ssl
import os

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""{CYAN}
   ╔═══════════════════════════════════╗
   ║    {GREEN}BUG MULTI-CHECKER by NamyDevx{CYAN}    ║
   ║       {YELLOW}Support HTTP • Payload • WS • DNS{CYAN} ║
   ╚═══════════════════════════════════╝{RESET}
""")

def load_bug_list(filename="list-bug.txt"):
    try:
        with open(filename, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"{RED}❌ File '{filename}' tidak ditemukan.{RESET}")
        return []

def check_bug(host):
    url = f"https://{host}"
    try:
        response = requests.get(url, timeout=5)
        code = response.status_code
        if code == 101:
            return f"🧩 {host} — Switching Protocols ({code})"
        elif code in [200, 301, 302]:
            return f"✅ {host} — LIVE ({code})"
        elif code == 403:
            return f"⚠️ {host} — Terlarang ({code})"
        else:
            return f"❌ {host} — Gagal ({code})"
    except requests.exceptions.RequestException:
        return f"❌ {host} — Timeout / Tidak Terhubung"

def check_bug_with_payload(host):
    url = f"https://{host}"
    headers = {
        "Host": host,
        "X-Online-Host": host,
        "User-Agent": "Mozilla/5.0",
        "Connection": "keep-alive"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        code = response.status_code
        if code == 101:
            return f"🧩 {host} — Switching Protocols via payload ({code})"
        elif code in [200, 301, 302]:
            return f"✅ {host} — LIVE via payload ({code})"
        elif code == 403:
            return f"⚠️ {host} — Terlarang via payload ({code})"
        else:
            return f"❌ {host} — Gagal via payload ({code})"
    except requests.exceptions.RequestException:
        return f"❌ {host} — Timeout via payload"

def check_websocket_upgrade(host):
    try:
        sock = socket.create_connection((host, 443), timeout=5)
        context = ssl.create_default_context()
        ssock = context.wrap_socket(sock, server_hostname=host)
        upgrade_request = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            "Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        ssock.send(upgrade_request.encode())
        response = ssock.recv(1024).decode()
        ssock.close()
        if "101 Switching Protocols" in response:
            return f"🧩 {host} — Mendukung WebSocket (101)"
        else:
            return f"❌ {host} — Tidak support WebSocket"
    except Exception:
        return f"❌ {host} — Error saat tes WebSocket"

def check_sni_redirect(host):
    try:
        ip = socket.gethostbyname(host)
        if ip.startswith("10.") or ip.startswith("100.") or ip.startswith("192.168") or ip.startswith("172."):
            return f"🔄 {host} — Redirect ke IP lokal: {ip}"
        elif ip.startswith("36.") or ip.startswith("180.") or ip.startswith("114."):
            return f"🛡️ {host} — Mungkin injeksi ISP (IP: {ip})"
        else:
            return f"✅ {host} — IP: {ip}"
    except Exception:
        return f"❌ {host} — Tidak dapat resolve DNS"

def main():
    clear()
    banner()
    bug_list = load_bug_list()
    if not bug_list:
        return

    print(f"{CYAN}Pilih Mode:{RESET}")
    print(f"{GREEN}[1]{RESET} HTTP Normal")
    print(f"{GREEN}[2]{RESET} Pakai Payload")
    print(f"{GREEN}[3]{RESET} WebSocket Upgrade")
    print(f"{GREEN}[4]{RESET} Cek Redirect / Injeksi DNS\n")

    mode = input(f"{YELLOW}Pilih mode (1-4): {RESET}").strip()
    print()

    start = time.time()
    with ThreadPoolExecutor(max_workers=10) as executor:
        if mode == "2":
            results = executor.map(check_bug_with_payload, bug_list)
        elif mode == "3":
            results = executor.map(check_websocket_upgrade, bug_list)
        elif mode == "4":
            results = executor.map(check_sni_redirect, bug_list)
        else:
            results = executor.map(check_bug, bug_list)

    for result in results:
        print(result)

    print(f"\n{CYAN}Selesai dalam {round(time.time() - start, 2)} detik.{RESET}")

if __name__ == "__main__":
    main()""
