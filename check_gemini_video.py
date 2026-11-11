"""
Direct Gemini test: Type, send, and wait for response streaming.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"

def main():
    print("Connecting to Gemini session...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://gemini.google.com/app", timeout=45000)
        
        # Click on the input container
        input_elem = page.locator("[contenteditable='true']").first
        input_elem.click()
        input_elem.type("Can you generate an animated video file directly in this chat, or do you only generate text and images?", delay=25)
        time.sleep(1)
        
        # Press Enter to send
        page.keyboard.press("Enter")
        print("Prompt typed and sent! Waiting 20 seconds for response...")
        time.sleep(20)
        
        os.makedirs("output/debug", exist_ok=True)
        screenshot = "output/debug/gemini_capability_check.png"
        page.screenshot(path=screenshot)
        print(f"Captured screenshot at: {screenshot}")
        
        browser.close()

if __name__ == "__main__":
    main()
