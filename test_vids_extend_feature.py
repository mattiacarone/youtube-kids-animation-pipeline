"""
Tests generating a continuous welcoming video in Google Vids and exploring the 'Extend' feature.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/create"

WELCOMING_PROMPT = (
    "Cute 3D Pixar preschool cartoon animation: Pixy, an adorable 5-year-old child explorer "
    "with messy brown hair and big expressive warm green eyes, wearing a bright yellow hoodie. "
    "Pixy looks directly into the camera with an affectionate, joyful, welcoming smile, waving both hands hello "
    "to the preschool children. Pixy holds up a magical glowing golden compass that gently sparkles with warm golden light beams. "
    "Seamless continuous motion, warm cozy lighting, Cocomelon preschool style."
)

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(VIDS_URL, timeout=45000)
        page.wait_for_timeout(4000)
        
        # Select Portrait format
        print("Selecting Portrait format...")
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
            
        page.keyboard.press("Escape")
        time.sleep(1)
        
        # Fill prompt
        print("Filling welcoming prompt...")
        textarea = page.locator("[role='textbox'][aria-label*='Describe your video'], [contenteditable='true']").first
        textarea.focus()
        textarea.click(force=True)
        textarea.fill(WELCOMING_PROMPT)
        time.sleep(1)
        
        # Click Generate
        print("Clicking Generate...")
        gen_btn = page.get_by_role("button", name="Generate", exact=True)
        gen_btn.click(force=True)
        
        print("Waiting for generation (35-45s)...")
        time.sleep(30)
        for i in range(25):
            btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
            if any(b.is_visible() for b in btns):
                print(f"Generated successfully in {30 + i*5}s!")
                break
            time.sleep(5)
            
        page.screenshot(path="output/debug/vids_welcoming_generated.png")
        print("Saved screenshot to output/debug/vids_welcoming_generated.png")
        
        # Check Extend button
        extend_btn = page.locator("button, [role='button']").filter(has_text="Extend").first
        if extend_btn.is_visible():
            print("Found Extend button! Inspecting properties...")
            extend_btn.click()
            time.sleep(2)
            page.screenshot(path="output/debug/vids_extend_clicked.png")
            print("Saved extend screenshot to output/debug/vids_extend_clicked.png")
            
        browser.close()

if __name__ == "__main__":
    main()

