import sys
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"

def main():
    print("Testing Playwright with .browser_session...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=USER_DATA_DIR,
                headless=True,
                channel="chrome",
                args=["--disable-blink-features=AutomationControlled"]
            )
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.goto("https://docs.google.com/videos/u/0/", timeout=30000)
            page.wait_for_timeout(3000)
            print("Successfully loaded Google Vids! Title:", page.title())
            browser.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
