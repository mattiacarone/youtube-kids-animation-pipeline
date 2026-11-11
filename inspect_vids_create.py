import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://docs.google.com/videos/create", timeout=45000)
        page.wait_for_timeout(5000)
        os.makedirs("output/debug", exist_ok=True)
        page.screenshot(path="output/debug/vids_create_screen.png")
        print("URL:", page.url)
        print("Title:", page.title())
        
        # Look for buttons
        buttons = page.locator("button, [role='button']").all()
        print(f"Found {len(buttons)} button elements:")
        for b in buttons:
            txt = b.inner_text().strip()
            aria = b.get_attribute("aria-label") or ""
            if txt or aria:
                print(f"  Button: '{txt}' | aria-label: '{aria}'")
        browser.close()

if __name__ == "__main__":
    main()
