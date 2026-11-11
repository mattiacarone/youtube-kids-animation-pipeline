"""
Automation runner for Gemini Web.
Uploads the image and submits prompt to Gemini.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"

def main():
    print("Launching automated Gemini session...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://gemini.google.com/app", wait_until="networkidle", timeout=30000)
        
        # Click on prompt area
        prompt_input = page.locator("rich-textarea, div[role='textbox'], p").first
        prompt_input.click()
        prompt_input.fill("Create a 5-second animated video of a cute 2D cartoon baby penguin waddling on ice, preschool animation style.")
        time.sleep(1)
        
        # Click send or press Enter
        page.keyboard.press("Enter")
        print("Prompt submitted to Gemini. Waiting for response...")
        time.sleep(15)
        
        os.makedirs("output/debug", exist_ok=True)
        page.screenshot(path="output/debug/gemini_response.png")
        print("Saved response screenshot to output/debug/gemini_response.png")
        
        browser.close()

if __name__ == "__main__":
    main()
