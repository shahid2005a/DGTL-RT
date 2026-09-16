import os
import sys
import time
import socket
import shutil
import subprocess
import ssl
import re
import json
import urllib.request
from urllib.parse import urlparse, urljoin

# --- COLORS ---
RED = "\033[91m"; GREEN = "\033[92m"; YELLOW = "\033[93m"
BLUE = "\033[94m"; CYAN = "\033[96m"; MAGENTA = "\033[95m"
RESET = "\033[0m"; BOLD = "\033[1m"; BG_RED = "\033[41m"

HOME = os.environ.get('HOME')
REPORT_DIR = f"{HOME}/DGTL_Reports"
SHOT_DIR = f"{HOME}/DGTL_Reports/Screenshots"


# ══════════════════════════════════════════════════════════
#  ENVIRONMENT DETECTION
# ══════════════════════════════════════════════════════════

def detect_env():
    if "com.termux" in os.environ.get("PREFIX", "") or os.path.exists("/data/data/com.termux"):
        return "termux"
    elif os.path.exists("/etc/os-release"):
        try:
            with open("/etc/os-release") as f:
                content = f.read().lower()
                if "kali" in content:
                    return "kali"
                elif "debian" in content or "ubuntu" in content:
                    return "debian"
        except Exception:
            pass
    return "linux"


ENV = detect_env()

if ENV == "termux":
    NIKTO_PATH = f"{HOME}/nikto/program/nikto.pl"
elif ENV == "kali":
    NIKTO_PATH = "/usr/bin/nikto"
else:
    NIKTO_PATH = shutil.which("nikto") or f"{HOME}/nikto/program/nikto.pl"


# ══════════════════════════════════════════════════════════
#  BANNER
# ══════════════════════════════════════════════════════════

def show_banner():
    banner_text = """
 ██████╗  ██████╗ ████████╗██╗         ██╗    ██╗███████╗██████╗ 
 ██╔══██╗██╔════╝ ╚══██╔══╝██║         ██║    ██║██╔════╝██╔══██╗
 ██║  ██║██║  ███╗   ██║   ██║         ██║ █╗ ██║█████╗  ██████╔╝
 ██║  ██║██║   ██║   ██║   ██║         ██║███╗██║██╔══╝  ██╔══██╗
 ██████╔╝╚██████╔╝   ██║   ███████╗    ╚███╔███╔╝███████╗██████╔╝
 ╚═════╝  ╚═════╝    ╚═╝   ╚══════╝     ╚══╝╚══╝ ╚══════╝╚═════╝ 

\033[1;93m┌────────────────────────────────────────────────────────────────┐\033[0m
\033[1;93m│\033[1;91m  🔴 \033[1;97mYouTube:\033[0m \033[1;96mhttps://www.youtube.com/@aryanafridi00\033[1;93m              │\033[0m
\033[1;93m│\033[1;92m  🌐 \033[1;97mGitHub:\033[0m \033[1;96mhttps://github.com/shahid2005a\033[1;93m                 │\033[0m
\033[1;93m│\033[1;95m  💻 \033[1;97mDeveloper:\033[0m \033[1;92mARYAN AFRIDI\033[1;93m                               │\033[0m
\033[1;93m└────────────────────────────────────────────────────────────────┘\033[0m
"""
    print(banner_text)
    print("\n")
    print("\033[1;92m╔════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[1;92m║\033[1;96m  ┌──────────────────────────────────────────────────┐\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;91m  🌐 \033[1;93m▐\033[1;91m█\033[1;93m▐\033[1;91m█\033[1;93m▐\033[1;91m█\033[1;93m▐ \033[1;97mFULL WEBSITE DEEP SCAN REPORT\033[1;96m  │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;92m  🌐 \033[1;93mURL & CONFIG EXTRACTOR\033[1;96m                      │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;94m  🧠 \033[1;93mDetected Technologies:\033[1;96m                  │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;95m  🔎 \033[1;91m🔎 \033[1;97mNIKTO FULL AUDIT\033[1;96m              │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;97m  📁 \033[1;93mHIDDEN DIRECTORY SCAN\033[1;96m                       │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;91m  📦 \033[1;93mOUTDATED SERVER SOFTWARE CHECK\033[1;96m                       │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;92m  ✅ \033[1;91mDEEP SCAN COMPLETE! \033[1;92m[✓] \033[1;97mENABLED\033[1;96m       │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  └──────────────────────────────────────────────────┘\033[1;92m  ║\033[0m")
    print("\033[1;92m╚════════════════════════════════════════════════════════════╝\033[0m")
    print("\n")
    print("\033[1;95m┌────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;95m│\033[1;97m  [\033[1;92m●\033[1;97m] \033[1;92mWEBSITE\033[1;97m  [\033[1;96m●\033[1;97m] \033[1;96mSeceen\033[1;97m  [\033[1;93m●\033[1;97m] \033[1;93mServe ip\033[1;97m  [\033[1;91m●\033[1;97m] \033[1;91mLIVE\033[1;97m  [\033[1;92m●\033[1;97m] \033[1;92mREADY\033[1;97m  │\033[0m")
    print("\033[1;95m│\033[1;92m  🚀 \033[1;97mSTATUS: \033[1;92mACTIVE\033[1;97m  │  \033[1;96m⚡ \033[1;97mSPEED: \033[1;93m20fps\033[1;97m  │  \033[1;91m📡 \033[1;97mSIGNAL: \033[1;92mSTRONG\033[1;97m  │\033[1;95m\033[0m")
    print("\033[1;95m└────────────────────────────────────────────────────────────┘\033[0m")
    print("\n")
    print("\033[1;91m▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\033[0m")
    print("\033[1;92m▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\033[0m")
    print("\033[1;93m████████████████████████████████████████████████████████████\033[0m")
    print("\n")


# ══════════════════════════════════════════════════════════
#  ENGINE SETUP
# ══════════════════════════════════════════════════════════

def fix_engine():
    for d in (REPORT_DIR, SHOT_DIR):
        if not os.path.exists(d):
            os.makedirs(d)

    print(f"{YELLOW}[*] Checking dependencies for {ENV}...{RESET}")

    if ENV == "termux":
        if shutil.which("perl") is None:
            os.system("pkg install perl -y")
        if shutil.which("whois") is None:
            os.system("pkg install whois -y >/dev/null 2>&1 || true")
        if shutil.which("git") is None:
            os.system("pkg install git -y")
        if not os.path.exists(NIKTO_PATH) and shutil.which("nikto") is None:
            os.system(f"git clone https://github.com/sullo/nikto {HOME}/nikto")
            os.system(f"chmod +x {NIKTO_PATH}")
    else:
        missing = []
        if shutil.which("nikto") is None:
            missing.append("nikto")
        if shutil.which("whois") is None:
            missing.append("whois")
        if shutil.which("git") is None:
            missing.append("git")
        if missing:
            print(f"{YELLOW}[*] Installing: {' '.join(missing)}{RESET}")
            os.system(f"sudo apt update -y >/dev/null 2>&1")
            os.system(f"sudo apt install {' '.join(missing)} -y")


def redirect_to_youtube():
    os.system('clear')
    print(f"{RED}{BOLD}[!] TOOL IS LOCKED!{RESET}")
    print(f"{YELLOW}Subscribe & hit the bell icon...{RESET}")
    for i in range(5, 0, -1):
        print(f"{RED}{i}...{RESET}", end=" ", flush=True)
        time.sleep(1)
    if ENV == "termux":
        os.system("termux-open https://www.youtube.com/@aryanafridi00?si=fEyQbmfEOGMl_3Xn")
    else:
        os.system("xdg-open https://www.youtube.com/@aryanafridi00?si=fEyQbmfEOGMl_3Xn 2>/dev/null &")
    input(f"\n{GREEN}[+] Press ENTER to unlock 🔓{RESET}")


# ══════════════════════════════════════════════════════════
#  UTILITIES
# ══════════════════════════════════════════════════════════

def clean_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
    return urlparse(url).hostname or url


def get_server_ip(hostname):
    try:
        ips = socket.getaddrinfo(hostname, None)
        return sorted(set(ip[4][0] for ip in ips))
    except socket.gaierror:
        return None


def fetch_url(url, timeout=10):
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            raw = resp.read()
            try:
                content = raw.decode("utf-8", errors="ignore")
            except Exception:
                content = raw.decode("latin-1", errors="ignore")
            return content, resp.status, dict(resp.headers)
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="ignore")
            return body, e.code, dict(e.headers)
        except Exception:
            return "", e.code, {}
    except Exception:
        return "", None, {}


def get_headers(hostname):
    for scheme in ("https", "http"):
        body, status, headers = fetch_url(f"{scheme}://{hostname}", timeout=15)
        if status:
            return headers, status, f"{scheme}://{hostname}", body
    return {}, None, None, ""


def get_whois_info(hostname):
    info = {}
    if shutil.which("whois") is None:
        return info
    try:
        out = subprocess.check_output(
            ["whois", hostname], stderr=subprocess.DEVNULL, timeout=20
        ).decode(errors="ignore")
        for line in out.splitlines():
            low = line.lower()
            if any(k in low for k in ["registrar:", "creation date:", "expiry",
                                       "expiration", "name server", "org:",
                                       "country:", "updated date", "status:",
                                       "registrant"]):
                info.setdefault("whois", []).append(line.strip())
    except Exception:
        pass
    return info


def get_technologies(headers, hostname):
    tech = []
    h = {k.lower(): v for k, v in headers.items()}
    server = h.get("server", "")
    powered = h.get("x-powered-by", "")
    if server:
        tech.append(f"Web Server : {server}")
    if powered:
        tech.append(f"Backend    : {powered}")
    if "cf-ray" in h or "cloudflare" in server.lower():
        tech.append("CDN        : Cloudflare")
    if "x-vercel" in h or "vercel" in server.lower():
        tech.append("Hosting    : Vercel")
    if "netlify" in server.lower():
        tech.append("Hosting    : Netlify")
    if "nginx" in server.lower():
        tech.append("Server     : Nginx")
    if "apache" in server.lower():
        tech.append("Server     : Apache")
    if "openresty" in server.lower():
        tech.append("Server     : OpenResty (Nginx+Lua)")
    if "cloudfront" in h.get("via", "").lower():
        tech.append("CDN        : AWS CloudFront")
    return tech


# ══════════════════════════════════════════════════════════
#  URL EXTRACTOR
# ══════════════════════════════════════════════════════════

URL_REGEX = re.compile(
    r'https?://[a-zA-Z0-9\.\-_~:/?#\[\]@!$&\'()*+,;=%]+',
    re.IGNORECASE
)

DOMAIN_REGEX = re.compile(
    r'\b([a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.)+[a-z]{2,}\b',
    re.IGNORECASE
)


def extract_all_urls_from_text(text):
    urls = set()
    domains = set()
    for m in URL_REGEX.finditer(text):
        url = m.group(0).rstrip(".,;:'\")\\")
        urls.add(url)
    for m in DOMAIN_REGEX.finditer(text):
        d = m.group(0).lower()
        if any(x in d for x in ["w3.org", "schema.org", "example.com", "googleapis.com",
                                  "gstatic.com", "google.com", "youtube.com",
                                  "facebook.com", "twitter.com", "w3schools.com",
                                  "jquery.com", "cloudflare.com", "jsdelivr.net",
                                  "cdnjs.com", "bootstrapcdn.com"]):
            continue
        domains.add(d)
    return urls, domains


def extract_all_links(html, base_url):
    js_urls = set(); css_urls = set(); json_urls = set(); all_urls = set()
    for m in re.finditer(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        all_urls.add(m.group(1))
    for m in re.finditer(r'<link[^>]+href\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        all_urls.add(m.group(1))
    for m in re.finditer(r'(?:src|href|data-src|data-href|action|poster)\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        all_urls.add(m.group(1))
    for m in re.finditer(r'["\']((?:https?:)?//[^"\']+)["\']', html):
        all_urls.add(m.group(1))
    for m in re.finditer(r'["\']([^"\']*\.js(?:\?[^"\']*)?)["\']', html):
        all_urls.add(m.group(1))
    for m in re.finditer(r'["\']([^"\']*\.css(?:\?[^"\']*)?)["\']', html):
        all_urls.add(m.group(1))
    for m in re.finditer(r'["\']([^"\']*\.json(?:\?[^"\']*)?)["\']', html):
        all_urls.add(m.group(1))

    base = base_url.rstrip("/")
    for url in all_urls:
        if not url or url.startswith(("#", "javascript:", "mailto:", "tel:", "data:")):
            continue
        if url.startswith("//"):
            url = "https:" + url
        elif url.startswith("/"):
            url = base + url
        elif not url.startswith("http"):
            url = base + "/" + url.lstrip("./")
        if url.endswith(".js") or ".js?" in url:
            js_urls.add(url)
        elif url.endswith(".css") or ".css?" in url:
            css_urls.add(url)
        elif url.endswith(".json") or ".json?" in url:
            json_urls.add(url)

    return js_urls, css_urls, json_urls, all_urls


def display_urls_and_configs(hostname, log, save_to=None):
    log(f"\n{YELLOW}{'='*60}{RESET}")
    log(f"{BOLD}{CYAN}       🌐 URL & CONFIG EXTRACTOR{RESET}")
    log(f"{YELLOW}{'='*60}{RESET}")

    all_urls = set(); all_domains = set(); all_configs = {}

    base = f"https://{hostname}"
    html, status, _ = fetch_url(base, timeout=15)
    if not html:
        html, status, _ = fetch_url(f"http://{hostname}", timeout=15)
        base = f"http://{hostname}"

    if html:
        log(f"{GREEN}[+] Homepage fetched ({len(html)} bytes){RESET}")
        urls, domains = extract_all_urls_from_text(html)
        all_urls.update(urls); all_domains.update(domains)

        js_urls, css_urls, json_urls, _ = extract_all_links(html, base)
        log(f"{GREEN}[+] Found {len(js_urls)} JS, {len(css_urls)} CSS, {len(json_urls)} JSON files{RESET}")

        for js in list(js_urls)[:30]:
            content, st, _ = fetch_url(js, timeout=8)
            if content:
                urls, domains = extract_all_urls_from_text(content)
                all_urls.update(urls); all_domains.update(domains)
                for m in re.finditer(
                    r'["\']([\w\-]*(?:api[Kk]ey|api[Uu]rl|auth[Dd]omain|project[Ii]d|'
                    r'database[Uu]rl|storage[Bb]ucket|config|endpoint|base[Uu]rl|'
                    r'token|secret|client[Ii]d)[\w\-]*)["\']\s*[:=]\s*["\']([^"\']{2,300})["\']',
                    content
                ):
                    all_configs[m.group(1)] = m.group(2)

    if all_urls:
        log(f"\n{GREEN}[+] 📎 All URLs Found ({len(all_urls)}):{RESET}")
        shown = 0
        for u in sorted(all_urls):
            if hostname in u and u.count("/") > 3:
                continue
            if shown >= 40:
                log(f"    {YELLOW}... aur {len(all_urls)-40} URLs (report me save){RESET}")
                break
            log(f"    {CYAN}➜ {u}{RESET}")
            shown += 1

    if all_domains:
        log(f"\n{GREEN}[+] 🌍 Unique Domains Found ({len(all_domains)}):{RESET}")
        for d in sorted(all_domains)[:50]:
            log(f"    {MAGENTA}➜ {d}{RESET}")

    if all_configs:
        log(f"\n{GREEN}[+] ⚙️  Config / Key-Value Pairs ({len(all_configs)}):{RESET}")
        for k, v in all_configs.items():
            if any(s in k.lower() for s in ["key", "token", "secret"]):
                masked = v[:6] + "..." + v[-4:] if len(v) > 12 else "***"
                log(f"    {BOLD}{CYAN}➜ {k}{RESET} = {YELLOW}{masked}{RESET}")
            else:
                log(f"    {BOLD}{CYAN}➜ {k}{RESET} = {v}")
    else:
        log(f"{YELLOW}    [!] Koi config-like key-value pair nahi mila{RESET}")

    if save_to:
        save_to.write("\n=== ALL URLS ===\n")
        for u in sorted(all_urls):
            save_to.write(f"{u}\n")
        save_to.write("\n=== UNIQUE DOMAINS ===\n")
        for d in sorted(all_domains):
            save_to.write(f"{d}\n")
        save_to.write("\n=== CONFIG KEY-VALUES ===\n")
        for k, v in all_configs.items():
            save_to.write(f"{k}: {v}\n")

    return all_urls, all_domains, all_configs


# ══════════════════════════════════════════════════════════
#  🔥 NIKTO (ULTRA FAST — 10 SEC)
# ══════════════════════════════════════════════════════════

def run_nikto(hostname, extra_args, out_file, title, log):
    """🔥 Nikto ULTRA FAST — max 10 seconds"""
    log(f"\n{YELLOW}{'='*60}{RESET}")
    log(f"{BOLD}{CYAN}       {title}{RESET}")
    log(f"{YELLOW}{'='*60}{RESET}")

    # ULTRA FAST: maxtime 10, timeout 30
    if ENV == "termux":
        cmd = (f"perl {NIKTO_PATH} -h {hostname} {extra_args} "
               f"-maxtime 10 -nointeractive -o {out_file} -Format txt 2>&1")
    else:
        cmd = (f"nikto -h {hostname} {extra_args} "
               f"-maxtime 10 -nointeractive -o {out_file} -Format txt 2>&1")

    log(f"{GREEN}[*] Running (max 10 sec)...{RESET}")

    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True,
                              text=True, timeout=30)
        output = proc.stdout + proc.stderr

        printed = 0
        for line in output.splitlines():
            if line.strip() and printed < 30:
                if any(kw in line for kw in ["+ ", "ERROR", "Target", "Server:",
                                              "OSVDB", "Allowed", "Retrieved",
                                              "No web server", "0 host",
                                              "host(s) tested"]):
                    log(f"    {line}")
                    printed += 1

        if os.path.exists(out_file) and os.path.getsize(out_file) > 0:
            log(f"{GREEN}[+] Report saved: {out_file}{RESET}")
        else:
            log(f"{YELLOW}[!] Report empty{RESET}")

    except subprocess.TimeoutExpired:
        log(f"{YELLOW}[!] Nikto timeout (30s) — aage badh rahe hai{RESET}")
    except Exception as e:
        log(f"{RED}[!] Nikto error: {e}{RESET}")


# ══════════════════════════════════════════════════════════
#  FULL DEEP SCAN
# ══════════════════════════════════════════════════════════

def full_deep_scan(target):
    hostname = clean_url(target)
    report_file = f"{REPORT_DIR}/{hostname.replace('.', '_')}_FULL_SCAN.txt"

    class Tee:
        def __init__(self, path):
            self.f = open(path, "w", encoding="utf-8")
        def write(self, s):
            self.f.write(s)
            self.f.flush()
        def close(self):
            self.f.close()

    tee = Tee(report_file)

    def log(msg=""):
        print(msg)
        tee.write(msg + "\n")

    log(f"\n{MAGENTA}{'='*60}{RESET}")
    log(f"{BOLD}{CYAN}       🌐 FULL WEBSITE DEEP SCAN REPORT{RESET}")
    log(f"{MAGENTA}{'='*60}{RESET}")
    log(f"{GREEN}[+] Target URL      :{RESET} {BOLD}{target}{RESET}")
    log(f"{GREEN}[+] Hostname        :{RESET} {BOLD}{hostname}{RESET}")
    log(f"{GREEN}[+] Environment     :{RESET} {BOLD}{ENV.upper()}{RESET}")
    log(f"{GREEN}[+] Scan Time       :{RESET} {time.strftime('%Y-%m-%d %H:%M:%S')}")

    log(f"\n{YELLOW}[*] Resolving DNS...{RESET}")
    ips = get_server_ip(hostname)
    ipv4 = None
    if ips:
        log(f"{GREEN}[+] Server IP Address(es):{RESET}")
        for ip in ips:
            tag = "IPv6" if ":" in ip else "IPv4"
            log(f"    {BOLD}{CYAN}➜ {ip}  ({tag}){RESET}")
            if ":" not in ip and ipv4 is None:
                ipv4 = ip
    else:
        log(f"{RED}    ❌ DNS resolve nahi hua!{RESET}")

    if ipv4:
        try:
            rev = socket.gethostbyaddr(ipv4)
            log(f"{GREEN}[+] Reverse DNS    :{RESET} {rev[0]}")
        except Exception:
            pass

    log(f"\n{YELLOW}[*] Fetching HTTP Headers...{RESET}")
    headers, status, final_url, _ = get_headers(hostname)
    if headers:
        log(f"{GREEN}[+] HTTP Status     :{RESET} {status}")
        log(f"{GREEN}[+] Final URL      :{RESET} {final_url}")
        log(f"{GREEN}[+] Full Headers   :{RESET}")
        for k, v in headers.items():
            log(f"    {CYAN}➜ {k}:{RESET} {v}")

    tech = get_technologies(headers, hostname)
    if tech:
        log(f"\n{GREEN}[+] 🧠 Detected Technologies:{RESET}")
        for t in tech:
            log(f"    {MAGENTA}➜ {t}{RESET}")

    log(f"\n{YELLOW}[*] WHOIS Lookup...{RESET}")
    if shutil.which("whois"):
        whois_info = get_whois_info(hostname)
        if whois_info.get("whois"):
            for line in whois_info["whois"][:20]:
                log(f"    {CYAN}➜ {line}{RESET}")
        else:
            log(f"{YELLOW}    [!] WHOIS data nahi mila{RESET}")

    # URL + Config extractor
    display_urls_and_configs(hostname, log, save_to=tee)

    # Nikto (ULTRA FAST — 10 sec each)
    nikto_out = f"{REPORT_DIR}/{hostname.replace('.','_')}_nikto.txt"
    dir_out = f"{REPORT_DIR}/{hostname.replace('.','_')}_dirs.txt"
    outdated_out = f"{REPORT_DIR}/{hostname.replace('.','_')}_outdated.txt"

    run_nikto(hostname, "", nikto_out, "🔎 NIKTO FULL AUDIT", log)
    run_nikto(hostname, "-mutate 1 -Cgidirs all -Tuning 1", dir_out, "📁 HIDDEN DIRECTORY SCAN", log)
    run_nikto(hostname, "-Tuning b", outdated_out, "📦 OUTDATED SERVER SOFTWARE CHECK", log)

    log(f"\n{MAGENTA}{'='*60}{RESET}")
    log(f"{BOLD}{GREEN}       ✅ DEEP SCAN COMPLETE!{RESET}")
    log(f"{MAGENTA}{'='*60}{RESET}")
    log(f"{YELLOW}[*] Main Report  : {report_file}{RESET}")
    log(f"{YELLOW}[*] Nikto Report : {nikto_out}{RESET}")
    log(f"{YELLOW}[*] Dir Report   : {dir_out}{RESET}")
    log(f"{YELLOW}[*] Software Rpt : {outdated_out}{RESET}")

    tee.close()


# ══════════════════════════════════════════════════════════
#  MAIN DASHBOARD
# ══════════════════════════════════════════════════════════

def main_dashboard():
    os.system('clear')
    show_banner()
    print(f"\n{CYAN}[*] Environment: {BOLD}{ENV.upper()}{RESET}")
    print(f"{BLUE}[1]{RESET} 🌐 Full Website Deep Scan (All-in-One)")
    print(f"{BLUE}[2]{RESET} ❌ Exit")

    choice = input(f"\n{YELLOW}[?] Select an option: {RESET}").strip()

    if choice == '1':
        target = input(f"{BLUE}[*] Enter Website URL: {RESET}").strip()
        if not target:
            print(f"{RED}[!] Empty URL!{RESET}")
            time.sleep(2)
            main_dashboard(); return
        full_deep_scan(target)
        input(f"\n{YELLOW}Press Enter to return to menu...{RESET}")
        main_dashboard()
    elif choice == '2':
        print(f"{GREEN}Bye! Subscribe karna mat bhoolna 😎{RESET}")
        sys.exit()
    else:
        print(f"{RED}[!] Invalid choice.{RESET}")
        time.sleep(2)
        main_dashboard()


if __name__ == "__main__":
    redirect_to_youtube()
    fix_engine()
    main_dashboard()
