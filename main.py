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
REPORT_DIR = f"{HOME}/HCO_Reports"
SHOT_DIR = f"{HOME}/HCO_Reports/Screenshots"


# ══════════════════════════════════════════════════════════
#  🔥 ENVIRONMENT DETECTION (Kali vs Termux)
# ══════════════════════════════════════════════════════════

def detect_env():
    """Kali Linux ya Termux detect karo"""
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

# Nikto path per environment
if ENV == "termux":
    NIKTO_PATH = f"{HOME}/nikto/program/nikto.pl"
    NIKTO_CMD = f"perl {NIKTO_PATH}"
elif ENV == "kali":
    NIKTO_PATH = "/usr/bin/nikto"
    NIKTO_CMD = "nikto"
else:
    NIKTO_PATH = shutil.which("nikto") or f"{HOME}/nikto/program/nikto.pl"
    NIKTO_CMD = NIKTO_PATH

# Package manager
PKG_MGR = "pkg" if ENV == "termux" else "sudo apt"
INSTALL_FLAG = "-y" if ENV == "termux" else "-y"


# ══════════════════════════════════════════════════════════
#  🔥 NEW BANNER (as requested)
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

    # Advanced Matrix-Style Box
    print("\033[1;92m╔════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[1;92m║\033[1;96m  ┌──────────────────────────────────────────────────┐\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;91m  ⚡ \033[1;93m▐\033[1;91m█\033[1;93m▐\033[1;91m█\033[1;93m▐\033[1;91m█\033[1;93m▐ \033[1;97mFULL WEBSITE DEEP SCAN REPORT\033[1;96m  │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;92m  ⚡ \033[1;93m20FIREBASE PROJECT HUNTER\033[1;96m                      │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;94m  📸 \033[1;93mQUALITY: 0.85 (OPTIMIZED)\033[1;96m                  │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;95m  💕 \033[1;91m❤️ \033[1;97mCONNECTED TO: CUTE GIRL\033[1;96m              │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;97m  📁 \033[1;93m~/Pictures/DGTL_CAM/\033[1;96m                       │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;91m  🟥 \033[1;93mLIVE  ️🎥 BATCH SEND\033[1;96m                       │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  │\033[1;92m  🌐 \033[1;91mCLOUDFLARE TUNNEL: \033[1;92m[✓] \033[1;97mENABLED\033[1;96m       │\033[1;92m  ║\033[0m")
    print("\033[1;92m║\033[1;96m  └──────────────────────────────────────────────────┘\033[1;92m  ║\033[0m")
    print("\033[1;92m╚════════════════════════════════════════════════════════════╝\033[0m")

    print("\n")

    # Advanced Cyber Status Bar
    print("\033[1;95m┌────────────────────────────────────────────────────────────┐\033[0m")
    print("\033[1;95m│\033[1;97m  [\033[1;92m●\033[1;97m] \033[1;92mSYSTEM\033[1;97m  [\033[1;96m●\033[1;97m] \033[1;96mNETWORK\033[1;97m  [\033[1;93m●\033[1;97m] \033[1;93m Config\033[1;97m  [\033[1;91m●\033[1;97m] \033[1;91mLIVE\033[1;97m  [\033[1;92m●\033[1;97m] \033[1;92mREADY\033[1;97m  │\033[0m")
    print("\033[1;95m│\033[1;92m  🚀 \033[1;97mSTATUS: \033[1;92mACTIVE\033[1;97m  │  \033[1;96m⚡ \033[1;97mSPEED: \033[1;93m20fps\033[1;97m  │  \033[1;91m📡 \033[1;97mSIGNAL: \033[1;92mSTRONG\033[1;97m  │\033[1;95m\033[0m")
    print("\033[1;95m└────────────────────────────────────────────────────────────┘\033[0m")
    print("\n")

    # Glitch Effect Line
    print("\033[1;91m▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒\033[0m")
    print("\033[1;92m▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓\033[0m")
    print("\033[1;93m████████████████████████████████████████████████████████████\033[0m")
    print("\n")


# ══════════════════════════════════════════════════════════
#  🔥 ENGINE SETUP
# ══════════════════════════════════════════════════════════

def fix_engine():
    """Dono environments ke liye dependencies install karo"""
    for d in (REPORT_DIR, SHOT_DIR):
        if not os.path.exists(d):
            os.makedirs(d)

    print(f"{YELLOW}[*] Checking dependencies for {ENV}...{RESET}")

    if ENV == "termux":
        if shutil.which("perl") is None:
            print(f"{YELLOW}[*] Installing perl...{RESET}")
            os.system("pkg install perl -y")

        if shutil.which("whois") is None:
            print(f"{YELLOW}[*] Installing whois...{RESET}")
            os.system("pkg install whois -y >/dev/null 2>&1 || true")

        if shutil.which("git") is None:
            os.system("pkg install git -y")

        if not os.path.exists(NIKTO_PATH) and shutil.which("nikto") is None:
            print(f"{YELLOW}[*] Cloning Nikto...{RESET}")
            os.system(f"git clone https://github.com/sullo/nikto {HOME}/nikto")
            os.system(f"chmod +x {NIKTO_PATH}")

        try:
            import playwright
        except ImportError:
            print(f"{YELLOW}[!] Playwright install nahi hai (optional).{RESET}")
            print(f"{YELLOW}    Termux me try: pip install playwright && playwright install chromium{RESET}")

    else:
        # KALI / DEBIAN / UBUNTU
        missing = []
        if shutil.which("nikto") is None:
            missing.append("nikto")
        if shutil.which("whois") is None:
            missing.append("whois")
        if shutil.which("git") is None:
            missing.append("git")
        if shutil.which("curl") is None:
            missing.append("curl")

        if missing:
            print(f"{YELLOW}[*] Installing: {' '.join(missing)}{RESET}")
            os.system(f"sudo apt update -y >/dev/null 2>&1")
            os.system(f"sudo apt install {' '.join(missing)} -y")

        try:
            import playwright
            print(f"{GREEN}[+] Playwright available!{RESET}")
        except ImportError:
            print(f"{YELLOW}[!] Playwright install nahi hai (optional but recommended).{RESET}")
            print(f"{YELLOW}    Install: pip3 install playwright && playwright install chromium && playwright install-deps chromium{RESET}")

        if shutil.which("trufflehog") is None:
            print(f"{YELLOW}[!] TruffleHog nahi hai (optional). Install: pip3 install trufflehog{RESET}")


def redirect_to_youtube():
    os.system('clear')
    print(f"{RED}{BOLD}[!] TOOL IS LOCKED!{RESET}")
    print(f"{YELLOW}Subscribe & hit the bell icon...{RESET}")
    for i in range(5, 0, -1):
        print(f"{RED}{i}...{RESET}", end=" ", flush=True)
        time.sleep(1)
    if ENV == "termux":
        os.system("termux-open https://youtube.com/@hackers_colony_tech?si=fEyQbmfEOGMl_3Xn")
    else:
        os.system("xdg-open https://youtube.com/@hackers_colony_tech?si=fEyQbmfEOGMl_3Xn 2>/dev/null &")
    input(f"\n{GREEN}[+] Press ENTER to unlock 🔓{RESET}")


# ══════════════════════════════════════════════════════════
#  UTILITY FUNCTIONS
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
            "Accept-Language": "en-US,en;q=0.5",
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
    if "github" in server.lower():
        tech.append("Hosting    : GitHub Pages")
    if "nginx" in server.lower():
        tech.append("Server     : Nginx")
    if "apache" in server.lower():
        tech.append("Server     : Apache")
    if "openresty" in server.lower():
        tech.append("Server     : OpenResty (Nginx+Lua)")
    if "cloudfront" in h.get("via", "").lower():
        tech.append("CDN        : AWS CloudFront")
    if "x-amz" in " ".join(h.keys()):
        tech.append("Cloud      : AWS")
    if "set-cookie" in h and "phpsessid" in h["set-cookie"].lower():
        tech.append("Backend    : PHP")
    return tech


# ══════════════════════════════════════════════════════════
#  🔥 FIREBASE HUNTER
# ══════════════════════════════════════════════════════════

FIREBASE_PATTERNS = {
    "apiKey": r'apiKey["\']?\s*[:=]\s*["\']([^"\']{20,})["\']',
    "authDomain": r'authDomain["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    "projectId": r'projectId["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    "storageBucket": r'storageBucket["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    "messagingSenderId": r'messagingSenderId["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    "appId": r'appId["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    "databaseURL": r'databaseURL["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    "measurementId": r'measurementId["\']?\s*[:=]\s*["\']([^"\']+)["\']',
}

FB_URL_REGEX = re.compile(
    r'(?:https?://)?([a-z0-9\-]+)\.(firebaseapp\.com|web\.app|firebaseio\.com|cloudfunctions\.net|appspot\.com)',
    re.IGNORECASE
)

FB_APIKEY_REGEX = re.compile(r'AIza[0-9A-Za-z\-_]{35}')
FB_PROJECT_HINTS = re.compile(
    r'([a-z0-9\-]+)(?:-default-rtdb)?\.firebaseio\.com',
    re.IGNORECASE
)

FIREBASE_PATHS = [
    "/__/firebase/init.json",
    "/__/firebase/init.js",
    "/firebase-config.js",
    "/firebase-config.json",
    "/firebase.js",
    "/firebase-messaging-sw.js",
    "/service-worker.js",
    "/sw.js",
    "/config.js",
    "/config.json",
    "/app.js",
    "/main.js",
    "/bundle.js",
    "/static/js/main.js",
    "/assets/js/main.js",
    "/js/main.js",
    "/js/app.js",
    "/js/config.js",
    "/env.js",
    "/.env",
    "/manifest.json",
    "/firebase.json",
    "/assets/index.js",
    "/static/js/bundle.js",
    "/build/static/js/main.js",
]


def extract_firebase_from_text(text):
    found = {}
    for key, pat in FIREBASE_PATTERNS.items():
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            found[key] = m.group(1)

    if "apiKey" not in found:
        m = FB_APIKEY_REGEX.search(text)
        if m:
            found["apiKey"] = m.group(0)

    urls = set()
    for m in FB_URL_REGEX.finditer(text):
        urls.add(m.group(0).replace("https://", "").replace("http://", ""))

    if "projectId" not in found:
        m = FB_PROJECT_HINTS.search(text)
        if m:
            found["projectId"] = m.group(1)

    return found, urls


def extract_all_links(html, base_url):
    js_urls = set()
    all_urls = set()

    for m in re.finditer(r'<script[^>]+src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        all_urls.add(m.group(1))
    for m in re.finditer(r'<link[^>]+href\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        all_urls.add(m.group(1))
    for m in re.finditer(r'(?:src|href|data-src|data-href|action)\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        all_urls.add(m.group(1))
    for m in re.finditer(r'["\']((?:https?:)?//[^"\']+)["\']', html):
        all_urls.add(m.group(1))
    for m in re.finditer(r'["\']([^"\']*\.js(?:\?[^"\']*)?)["\']', html):
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

    return js_urls, all_urls


def hunt_firebase_playwright(hostname):
    """Playwright se deep scan (Kali me best kaam karta hai)"""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {}, set(), []

    all_config = {}
    all_fb_urls = set()
    all_js_urls = set()
    all_responses_text = ""

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox",
                      "--disable-dev-shm-usage"]
            )
            ctx = browser.new_context(
                user_agent=("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                            "Chrome/120 Safari/537.36"),
                ignore_https_errors=True,
                viewport={"width": 1366, "height": 768},
            )
            page = ctx.new_page()

            def on_request(req):
                url = req.url
                m = FB_URL_REGEX.search(url)
                if m:
                    all_fb_urls.add(m.group(0).replace("https://", "").replace("http://", ""))
                if url.endswith(".js") or ".js?" in url:
                    all_js_urls.add(url)

            def on_response(resp):
                nonlocal all_responses_text
                try:
                    url = resp.url
                    if url.endswith(".js") or ".js?" in url or "firebase" in url.lower():
                        text = resp.text()
                        if text and len(text) < 3_000_000:
                            all_responses_text += "\n" + text
                except Exception:
                    pass

            page.on("request", on_request)
            page.on("response", on_response)

            print(f"{CYAN}[*] Opening website in Chromium...{RESET}")
            try:
                page.goto(f"https://{hostname}", timeout=60000,
                          wait_until="domcontentloaded")
            except Exception:
                try:
                    page.goto(f"http://{hostname}", timeout=60000,
                              wait_until="domcontentloaded")
                except Exception:
                    pass

            print(f"{CYAN}[*] Waiting for JS to execute (12s)...{RESET}")
            time.sleep(12)

            try:
                for _ in range(4):
                    page.mouse.wheel(0, 2500)
                    time.sleep(1)
            except Exception:
                pass

            try:
                rendered_html = page.content()
                cfg, urls = extract_firebase_from_text(rendered_html)
                all_config.update(cfg)
                all_fb_urls.update(urls)
            except Exception:
                pass

            try:
                ls = page.evaluate("() => JSON.stringify(localStorage)")
                ss = page.evaluate("() => JSON.stringify(sessionStorage)")
                for store in (ls, ss):
                    if store:
                        cfg, urls = extract_firebase_from_text(store)
                        all_config.update(cfg)
                        all_fb_urls.update(urls)
            except Exception:
                pass

            try:
                win_str = page.evaluate("""() => {
                    try {
                        let out = {};
                        for (let k in window) {
                            try {
                                if (k.toLowerCase().includes('firebase') ||
                                    k.toLowerCase().includes('config') ||
                                    k.toLowerCase().includes('env')) {
                                    out[k] = JSON.stringify(window[k]).substring(0, 1000);
                                }
                            } catch(e) {}
                        }
                        return JSON.stringify(out);
                    } catch(e) { return ''; }
                }""")
                if win_str:
                    cfg, urls = extract_firebase_from_text(win_str)
                    all_config.update(cfg)
                    all_fb_urls.update(urls)
            except Exception:
                pass

            shot_path = f"{SHOT_DIR}/{hostname.replace('.', '_')}.png"
            try:
                page.screenshot(path=shot_path, full_page=True)
                print(f"{GREEN}[+] Screenshot: {shot_path}{RESET}")
            except Exception:
                pass

            browser.close()
    except Exception as e:
        print(f"{RED}[!] Playwright error: {e}{RESET}")

    if all_responses_text:
        cfg, urls = extract_firebase_from_text(all_responses_text)
        all_config.update(cfg)
        all_fb_urls.update(urls)

    for js_url in list(all_js_urls)[:40]:
        try:
            content, _, _ = fetch_url(js_url, timeout=8)
            if content:
                cfg, urls = extract_firebase_from_text(content)
                all_config.update(cfg)
                all_fb_urls.update(urls)
        except Exception:
            continue

    return all_config, all_fb_urls, list(all_js_urls)


def hunt_firebase(hostname):
    """Multi-layer Firebase hunter"""
    all_cfg = {}
    all_urls = set()
    all_js = []
    config_files = []

    base_https = f"https://{hostname}"

    print(f"{CYAN}[*] Fetching homepage...{RESET}")
    html, status, _ = fetch_url(base_https, timeout=15)
    if not html:
        html, status, _ = fetch_url(f"http://{hostname}", timeout=15)
        base_https = f"http://{hostname}"

    if html:
        print(f"{GREEN}[+] Homepage fetched ({len(html)} bytes){RESET}")
        cfg, urls = extract_firebase_from_text(html)
        all_cfg.update(cfg)
        all_urls.update(urls)

        js_links, all_links = extract_all_links(html, base_https)
        print(f"{CYAN}[*] Found {len(js_links)} JS files in HTML{RESET}")

        scan_targets = list(js_links)
        for u in all_links:
            if u.endswith(".json") or ".json?" in u:
                scan_targets.append(u)

        print(f"{CYAN}[*] Scanning {len(scan_targets)} JS/JSON files...{RESET}")
        for js_url in scan_targets[:80]:
            content, st, _ = fetch_url(js_url, timeout=8)
            if content:
                cfg, urls = extract_firebase_from_text(content)
                if cfg or urls:
                    all_cfg.update(cfg)
                    all_urls.update(urls)
                    all_js.append(js_url)
                    print(f"    {GREEN}✅ Firebase hint in: {js_url}{RESET}")
    else:
        print(f"{RED}[!] Homepage fetch fail!{RESET}")

    print(f"{CYAN}[*] Checking {len(FIREBASE_PATHS)} common config paths...{RESET}")
    for path in FIREBASE_PATHS:
        for scheme in ("https", "http"):
            url = f"{scheme}://{hostname}{path}"
            content, st, _ = fetch_url(url, timeout=6)
            if st and content and st == 200:
                cfg, urls = extract_firebase_from_text(content)
                if cfg or urls:
                    all_cfg.update(cfg)
                    all_urls.update(urls)
                    config_files.append(f"{url} [{st}]")
                    print(f"    {GREEN}✅ Found: {url} [{st}]{RESET}")
                    break
                elif len(content) > 0 and st == 200 and "firebase" in content.lower():
                    config_files.append(f"{url} [{st}] (no config)")
                    break

    if shutil.which("playwright") or os.path.exists(f"{HOME}/.cache/ms-playwright"):
        print(f"{CYAN}[*] Running Playwright deep scan...{RESET}")
        pw_cfg, pw_urls, pw_js = hunt_firebase_playwright(hostname)
        all_cfg.update(pw_cfg)
        all_urls.update(pw_urls)
        for j in pw_js:
            if j not in all_js:
                all_js.append(j)

    return all_cfg, all_urls, all_js, config_files


def check_url_live(url):
    content, status, _ = fetch_url(f"https://{url}", timeout=8)
    return status in (200, 403, 404)


def display_firebase_info(hostname, save_to=None):
    print(f"\n{YELLOW}{'='*60}{RESET}")
    print(f"{BOLD}{CYAN}       🔥 FIREBASE PROJECT HUNTER{RESET}")
    print(f"{YELLOW}{'='*60}{RESET}")

    all_cfg, all_urls, all_js, config_files = hunt_firebase(hostname)

    print(f"\n{YELLOW}[*] JS files scanned: {len(all_js)}{RESET}")
    if config_files:
        print(f"{GREEN}[+] Config files found: {len(config_files)}{RESET}")

    if not all_cfg and not all_urls:
        print(f"{RED}    ❌ Firebase config nahi mila!{RESET}")
        print(f"{YELLOW}    Possible reasons:{RESET}")
        print(f"      - Site Firebase use nahi karti")
        print(f"      - Config server-side se aa raha hai")
        print(f"      - Config environment variable me hai")
        if save_to:
            save_to.write("\n=== FIREBASE ===\nNo Firebase config detected.\n")
        return

    print(f"{GREEN}[+] 🔥 FIREBASE DETECTED!{RESET}")
    print(f"{MAGENTA}{'-'*55}{RESET}")

    project_id = all_cfg.get("projectId")

    if project_id:
        print(f"    {BOLD}{CYAN}📦 Project ID      :{RESET} {BOLD}{GREEN}{project_id}{RESET}")
    if all_cfg.get("authDomain"):
        print(f"    {BOLD}{CYAN}🔐 Auth Domain     :{RESET} {all_cfg['authDomain']}")
    if all_cfg.get("databaseURL"):
        print(f"    {BOLD}{CYAN}🗄️  Database URL    :{RESET} {all_cfg['databaseURL']}")
    if all_cfg.get("storageBucket"):
        print(f"    {BOLD}{CYAN}📁 Storage Bucket  :{RESET} {all_cfg['storageBucket']}")
    if all_cfg.get("apiKey"):
        k = all_cfg["apiKey"]
        masked = k[:10] + "..." + k[-4:] if len(k) > 20 else k
        print(f"    {BOLD}{CYAN}🔑 API Key         :{RESET} {masked} {YELLOW}(masked){RESET}")
        print(f"    {BOLD}{CYAN}🔑 Full API Key    :{RESET} {YELLOW}{k}{RESET}")
    if all_cfg.get("messagingSenderId"):
        print(f"    {BOLD}{CYAN}📨 Sender ID       :{RESET} {all_cfg['messagingSenderId']}")
    if all_cfg.get("appId"):
        print(f"    {BOLD}{CYAN}📱 App ID          :{RESET} {all_cfg['appId']}")
    if all_cfg.get("measurementId"):
        print(f"    {BOLD}{CYAN}📊 Measurement ID  :{RESET} {all_cfg['measurementId']}")

    test_urls = set(all_urls)
    if project_id:
        test_urls.add(f"{project_id}.web.app")
        test_urls.add(f"{project_id}.firebaseapp.com")
        test_urls.add(f"{project_id}-default-rtdb.firebaseio.com")
        test_urls.add(f"{project_id}.appspot.com")

    if test_urls:
        print(f"\n{GREEN}[+] 🌐 Firebase URLs Found:{RESET}")
        for u in sorted(test_urls):
            live = check_url_live(u)
            status = f"{GREEN}✅ LIVE{RESET}" if live else f"{RED}❌{RESET}"
            print(f"       {BOLD}{MAGENTA}➜ https://{u}{RESET}  [{status}]")

    if config_files:
        print(f"\n{GREEN}[+] 📄 Config Files Found:{RESET}")
        for f in config_files:
            print(f"       {MAGENTA}➜ {f}{RESET}")

    print(f"{MAGENTA}{'-'*55}{RESET}")

    if save_to:
        save_to.write("\n=== FIREBASE CONFIG ===\n")
        for k, v in all_cfg.items():
            save_to.write(f"{k}: {v}\n")
        save_to.write("\nFirebase URLs:\n")
        for u in sorted(test_urls):
            save_to.write(f"https://{u}\n")
        if config_files:
            save_to.write("\nConfig Files:\n")
            for f in config_files:
                save_to.write(f"{f}\n")
        save_to.write("\nJS Files Scanned:\n")
        for j in all_js:
            save_to.write(f"{j}\n")


# ══════════════════════════════════════════════════════════
#  🔥 NIKTO RUNNER
# ══════════════════════════════════════════════════════════

def run_nikto(hostname, extra_args, out_file, title, log):
    log(f"\n{YELLOW}{'='*60}{RESET}")
    log(f"{BOLD}{CYAN}       {title}{RESET}")
    log(f"{YELLOW}{'='*60}{RESET}")

    if ENV == "termux":
        cmd = (f"perl {NIKTO_PATH} -h {hostname} {extra_args} "
               f"-o {out_file} -Format txt -nointeractive 2>&1")
    else:
        cmd = (f"nikto -h {hostname} {extra_args} "
               f"-o {out_file} -Format txt -nointeractive 2>&1")

    log(f"{GREEN}[*] Running: {cmd[:80]}...{RESET}")

    try:
        proc = subprocess.run(cmd, shell=True, capture_output=True,
                              text=True, timeout=900)
        output = proc.stdout + proc.stderr

        printed = 0
        for line in output.splitlines():
            if line.strip() and printed < 50:
                if any(kw in line for kw in ["+ ", "ERROR", "Target", "Server:",
                                              "OSVDB", "Allowed", "Retrieved",
                                              "No web server", "0 host",
                                              "Start Time", "End Time",
                                              "host(s) tested"]):
                    log(f"    {line}")
                    printed += 1

        if os.path.exists(out_file) and os.path.getsize(out_file) > 0:
            log(f"{GREEN}[+] Report saved: {out_file}{RESET}")
        else:
            log(f"{YELLOW}[!] Report file empty or not created{RESET}")

    except subprocess.TimeoutExpired:
        log(f"{RED}[!] Nikto timeout (15 min){RESET}")
    except Exception as e:
        log(f"{RED}[!] Nikto error: {e}{RESET}")


# ══════════════════════════════════════════════════════════
#  🔥 FULL DEEP SCAN
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
    else:
        log(f"{RED}    ❌ Headers fetch nahi hue!{RESET}")

    tech = get_technologies(headers, hostname)
    if tech:
        log(f"\n{GREEN}[+] 🧠 Detected Technologies:{RESET}")
        for t in tech:
            log(f"    {MAGENTA}➜ {t}{RESET}")

    log(f"\n{YELLOW}[*] WHOIS Lookup...{RESET}")
    if shutil.which("whois") is None:
        log(f"{RED}    [!] whois install nahi hai{RESET}")
    else:
        whois_info = get_whois_info(hostname)
        if whois_info.get("whois"):
            for line in whois_info["whois"][:20]:
                log(f"    {CYAN}➜ {line}{RESET}")
        else:
            log(f"{YELLOW}    [!] WHOIS data nahi mila{RESET}")

    display_firebase_info(hostname, save_to=tee)

    nikto_out = f"{REPORT_DIR}/{hostname.replace('.','_')}_nikto.txt"
    dir_out = f"{REPORT_DIR}/{hostname.replace('.','_')}_dirs.txt"
    outdated_out = f"{REPORT_DIR}/{hostname.replace('.','_')}_outdated.txt"

    run_nikto(hostname, "", nikto_out, "🔎 NIKTO FULL AUDIT", log)
    run_nikto(hostname, "-mutate 1 -Cgidirs all", dir_out, "📁 HIDDEN DIRECTORY SCAN", log)
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
    show_banner()   # 🔥 New banner
    print(f"\n{CYAN}[*] Environment: {BOLD}{ENV.upper()}{RESET}")
    print(f"{BG_RED}{' '*52}{RESET}")
    print(f"{BG_RED}{BOLD}{GREEN}       HCO WEBSITE VULNERABILITY FINDER           {RESET}{BG_RED}  {RESET}")
    print(f"{BG_RED}{' '*52}{RESET}")
    print(f"\n{BLUE}[1]{RESET} 🌐 Full Website Deep Scan (All-in-One)")
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