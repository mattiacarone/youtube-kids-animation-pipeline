"""
Triggers AI Video Generation in Google Vids targeting exact button name='Generate', exact=True.
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
    print("Launching Google Vids in active session...")
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
        
        # Select Portrait format
        print("Selecting Portrait...")
        portrait_btn = page.get_by_text("Portrait")
        if portrait_btn.is_visible():
            portrait_btn.click()
            time.sleep(1)
            
        # Select Create AI Videos
        print("Opening Create AI videos panel...")
        create_btn = page.get_by_text("Create AI videos")
        if create_btn.is_visible():
            create_btn.click()
            time.sleep(2)
            
        # Fill prompt
        print("Filling generation prompt...")
        textarea = page.locator("textarea, [contenteditable='true']").first
        textarea.click()
        textarea.fill(PROMPT)
        time.sleep(1)
        
        # Click the exact Generate button
        print("Clicking exact 'Generate' button...")
        gen_btn = page.get_by_role("button", name="Generate", exact=True)
        gen_btn.click()
        
        print("Generation successfully triggered in Google Vids! Waiting 40 seconds for rendering...")
        time.sleep(40)
        
        os.makedirs("output/debug", exist_ok=True)
        screenshot = "output/debug/vids_rendering_live.png"
        page.screenshot(path=screenshot)
        print(f"Captured render progress screenshot at: {screenshot}")
        
        browser.close()

if __name__ == "__main__":
    main()
