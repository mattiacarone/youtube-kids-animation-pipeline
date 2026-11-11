"""
Test Gemini Advanced login and tools.
"""
import os
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"

def main():
    print("Testing connection to Gemini...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://gemini.google.com/app", wait_until="networkidle", timeout=45000)
        
        print(f"Title: {page.title()}")
        print(f"URL: {page.url}")
        
        screenshot_path = "output/debug/gemini_session.png"
        page.screenshot(path=screenshot_path)
        print(f"Saved Gemini screenshot to: {screenshot_path}")
        
        browser.close()

if __name__ == "__main__":
    main()
