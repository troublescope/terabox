import json
import os
from playwright.sync_api import sync_playwright

EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]

def extract_cookie():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Visit TeraBox
        page.goto("https://www.terabox.com")

        # Click login button
        page.click('text=Sign in')
        page.wait_for_timeout(2000)

        # If "Use email" option appears
        if page.is_visible('text="Use email"'):
            page.click('text="Use email"')

        # Fill login form
        page.fill('input[type="text"]', EMAIL)
        page.fill('input[type="password"]', PASSWORD)
        page.click('button:has-text("Login")')

        page.wait_for_url("**/main*", timeout=30000)

        # Dump all cookies with full details
        raw_cookies = context.cookies()

        cookies = []
        for c in raw_cookies:
            cookies.append({
                "domain": c.get("domain"),
                "expirationDate": c.get("expires"),
                "hostOnly": not c.get("domain", "").startswith("."),
                "httpOnly": c.get("httpOnly", False),
                "name": c.get("name"),
                "path": c.get("path"),
                "sameSite": c.get("sameSite", None),
                "secure": c.get("secure", False),
                "session": not bool(c.get("expires")),
                "storeId": None,
                "value": c.get("value")
            })

        with open("cookie.json", "w") as f:
            json.dump(cookies, f, indent=2)

        print(f"[✓] Extracted {len(cookies)} cookies.")
        browser.close()

extract_cookie()
