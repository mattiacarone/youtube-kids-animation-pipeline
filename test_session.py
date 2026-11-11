"""
Test persistent session connectivity to Google Labs / VideoFX.
Checks if user login is active.
"""
import os
import sys
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"

def main():
    print(f"Loading persistent profile from {USER_DATA_DIR}...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://labs.google/fx/tools/videofx", wait_until="networkidle", timeout=45000)
        
        title = page.title()
        url = page.url
        print(f"Current page title: {title}")
        print(f"Current URL: {url}")
        
        # Save a screenshot to confirm login state visually
        os.makedirs("output/debug", exist_ok=True)
        screenshot_path = "output/debug/session_check.png"
        page.screenshot(path=screenshot_path)
        print(f"Saved diagnostic screenshot to: {screenshot_path}")
        
        browser.close()

if __name__ == "__main__":
    main()
