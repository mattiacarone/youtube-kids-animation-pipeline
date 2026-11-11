"""
Automated Gemini prompt dispatcher.
Inputs prompt into Gemini Advanced and captures response.
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
        
        # Locate the exact prompt editor
        box = page.locator("[aria-label='Enter a prompt for Gemini'], [contenteditable='true']").first
        box.click()
        box.fill("Create a 5-second video animation of a baby penguin waddling on ice, 2D cartoon preschool style.")
        time.sleep(1)
        
        # Submit prompt
        send_btn = page.locator("button[aria-label*='Send'], button[aria-label*='submit']").first
        if send_btn.is_visible():
            send_btn.click()
        else:
            page.keyboard.press("Enter")
            
        print("Prompt successfully submitted! Waiting for Gemini response...")
        time.sleep(20)
        
        os.makedirs("output/debug", exist_ok=True)
        screenshot = "output/debug/gemini_result.png"
        page.screenshot(path=screenshot)
        print(f"Captured response screenshot at: {screenshot}")
        
        browser.close()

if __name__ == "__main__":
    main()
