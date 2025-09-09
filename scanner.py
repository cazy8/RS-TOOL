# scanner.py
# DISCLAIMER: This script is for educational purposes only. Do not use against any system without explicit permission.

import socket
import requests
from threading import Thread, Lock
from queue import Queue

# A lock to prevent race conditions when printing to the console
print_lock = Lock()

def find_subdomains(domain, wordlist_path):
    """
    Finds valid subdomains for a given domain using a wordlist.
    """
    found_subdomains = set()
    q = Queue()

    # Read wordlist and populate the queue
    try:
        with open(wordlist_path, "r") as f:
            for line in f:
                sub = line.strip()
                q.put(sub)
    except FileNotFoundError:
        print(f"[!] Error: Wordlist not found at {wordlist_path}")
        return []

    def worker():
        while not q.empty():
            subdomain = q.get()
            full_domain = f"{subdomain}.{domain}"

            # Validation: check label length and full domain length
            labels = full_domain.split('.')
            if any(len(label) > 63 for label in labels):
                with print_lock:
                    print(f"[!] Skipping {full_domain}: label too long")
                q.task_done()
                continue

            if len(full_domain) > 253:
                with print_lock:
                    print(f"[!] Skipping {full_domain}: domain name too long")
                q.task_done()
                continue

            try:
                socket.gethostbyname(full_domain)
                with print_lock:
                    print(f"[+] Found Subdomain: {full_domain}")
                    found_subdomains.add(full_domain)
            except socket.gaierror:
                # Domain does not resolve, ignore
                pass
            except UnicodeEncodeError:
                # IDNA encoding failed, skip
                with print_lock:
                    print(f"[!] Skipping {full_domain}: encoding with 'idna' codec failed")
            q.task_done()

    # Start threads
    thread_count = 20  # Number of threads
    for _ in range(thread_count):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    q.join()  # Wait for the queue to be empty
    return list(found_subdomains)

def scan_ports(target, ports):
    """
    Scans a list of ports on a single target.
    """
    open_ports = []
    q = Queue()

    def worker():
        while not q.empty():
            port = q.get()
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(1)  # Timeout of 1 second
                result = sock.connect_ex((target, port))
                if result == 0:
                    with print_lock:
                        print(f"    [+] Port {port} is open on {target}")
                        open_ports.append(port)
            q.task_done()

    for port in ports:
        q.put(port)

    # Start threads
    thread_count = 10
    for _ in range(thread_count):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    q.join()
    return sorted(open_ports)


def find_directories(base_url, wordlist_path):
    """
    Finds valid directories or files on a web server using a wordlist.
    """
    found_dirs = []
    q = Queue()

    # Ensure the base URL has a scheme
    if not base_url.startswith("http"):
        base_url = f"http://{base_url}"

    # Read wordlist
    try:
        with open(wordlist_path, "r") as f:
            for line in f:
                path = line.strip()
                if path and not path.startswith('/'):
                    path = f"/{path}"
                q.put(path)
    except FileNotFoundError:
        print(f"[!] Error: Wordlist not found at {wordlist_path}")
        return []

    def worker():
        while not q.empty():
            path = q.get()
            url = f"{base_url}{path}"
            try:
                res = requests.get(url, timeout=3, allow_redirects=True)
                if res.status_code != 404:
                    with print_lock:
                        print(f"[+] Found: {url} (Status: {res.status_code})")
                        found_dirs.append(f"{url} [Status: {res.status_code}]")
            except requests.RequestException:
                pass
            q.task_done()

    # Start threads
    thread_count = 20
    for _ in range(thread_count):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    q.join()
    return found_dirs
