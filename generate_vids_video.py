"""
Automated Google Vids Video Generation script.
Uses Gemini Omni inside Google Vids to generate true AI animated video clips.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"

PROMPT = (
    "Cute 3D Pixar preschool cartoon animation: An adorable chubby baby penguin "
    "waddles happily across sparkling Antarctic snow, flapping its tiny flippers excitedly. "
    "Bright primary colors, sunny pastel turquoise icebergs, Cocomelon preschool style."
)

def main():
    print("Connecting to Google Vids with your Google AI Pro session...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://docs.google.com/videos/create", timeout=45000)
        page.wait_for_timeout(4000)
        
        # Select Portrait (9:16) format for Shorts
        print("Selecting Portrait format...")
        portrait_btn = page.get_by_text("Portrait")
        if portrait_btn.is_visible():
            portrait_btn.click()
            time.sleep(1)
            
        # Select Create AI Videos
        print("Opening AI Video panel (Omni)...")
        create_btn = page.get_by_text("Create AI videos")
        if create_btn.is_visible():
            create_btn.click()
            time.sleep(2)
            
        # Locate prompt textarea
        textarea = page.locator("textarea, [contenteditable='true']").first
        textarea.click()
        textarea.fill(PROMPT)
        time.sleep(1)
        
        # Click the Generate (arrow-up) button
        print("Submitting prompt to Gemini Omni video generator in Google Vids...")
        arrow_btn = page.locator("button:has(mat-icon), button:has(svg), button").filter(has_text="").last
        page.keyboard.press("Enter")
        time.sleep(1)
        
        # Also try clicking the submit button directly
        submit_btn = page.locator("button:has-text('arrow_upward'), button[aria-label*='generate'], button[aria-label*='submit'], button:has(svg)").last
        try:
            submit_btn.click(timeout=3000)
        except Exception:
            pass
            
        print("AI Video generation triggered! Waiting for initial status...")
        time.sleep(15)
        
        os.makedirs("output/debug", exist_ok=True)
        screenshot = "output/debug/vids_generating.png"
        page.screenshot(path=screenshot)
        print(f"Captured status screenshot at: {screenshot}")
        
        browser.close()

if __name__ == "__main__":
    main()
