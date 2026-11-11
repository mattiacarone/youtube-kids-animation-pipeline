"""
Generates a 100% continuous, seamless, uncut welcoming video using Google Vids and the Extend feature.
Shot 1: Pixy warmly welcomes the kids, waving hello with pure affection.
Shot 2 (Extended): Pixy introduces the magical golden compass as it glows with golden beams and stars.
Result: 1 single continuous video without cuts or stopping.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/create"
OUT_VIDEO = r"C:\Users\Mattia\YouTubeKids\assets\clips\pixy_welcoming_continuous.mp4"

PROMPT_PART1 = (
    "Cute 3D Pixar preschool cartoon animation: Pixy, an adorable 5-year-old child explorer "
    "with messy brown hair and big expressive warm green eyes, wearing a bright yellow hoodie with bear ears. "
    "Pixy looks directly into the camera with an affectionate, joyful, welcoming smile, waving both hands hello "
    "to the young children with pure warmth. Pixy steps forward gently into the cozy room. "
    "Seamless continuous camera, warm golden lighting, Cocomelon preschool style."
)

PROMPT_PART2 = (
    "Pixy smiles warmly, reaches forward and holds up the magical golden compass with both hands as it glows "
    "with warm golden light beams and gentle sparkling stars. Pixy looks into the camera with delighted wonder, "
    "smiling affectionately at the viewer. Seamless continuous shot, no cut, warm cozy room."
)

def main():
    os.makedirs(os.path.dirname(OUT_VIDEO), exist_ok=True)
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
        
        # 1. Select Portrait
        print("Selecting Portrait...")
        portrait_btn = page.get_by_text("Portrait")
        if portrait_btn.is_visible():
            portrait_btn.click()
            time.sleep(1)
            
        # 2. Open AI Videos
        print("Opening AI videos panel...")
        create_btn = page.get_by_text("Create AI videos")
        if create_btn.is_visible():
            create_btn.click()
            time.sleep(2)
            
        page.keyboard.press("Escape")
        time.sleep(1)
        
        # 3. Enter Part 1 Prompt
        print("Entering Part 1 prompt...")
        textarea = page.locator("[role='textbox'][aria-label*='Describe your video'], [contenteditable='true']").first
        textarea.focus()
        textarea.click(force=True)
        textarea.fill(PROMPT_PART1)
        time.sleep(1)
        
        # 4. Generate Part 1
        print("Generating Part 1...")
        gen_btn = page.get_by_role("button", name="Generate", exact=True)
        gen_btn.click(force=True)
        
        # Wait for Part 1 to finish
        print("Waiting for Part 1 rendering...")
        time.sleep(30)
        for i in range(25):
            btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
            if any(b.is_visible() for b in btns):
                print(f"Part 1 ready in {30 + i*5}s!")
                break
            time.sleep(5)
            
        page.screenshot(path="output/debug/continuous_part1_ready.png")
        
        # 5. Click Extend
        print("Clicking Extend button...")
        extend_btn = page.locator("button, [role='button']").filter(has_text="Extend").first
        extend_btn.click(force=True)
        time.sleep(2)
        
        # 6. Fill Extend Prompt
        print("Filling Extend prompt (Part 2)...")
        extend_box = page.locator("[role='textbox'][aria-label*='Create a video and describe'], [role='textbox'][aria-label*='Describe'], [contenteditable='true']").first
        extend_box.focus()
        extend_box.click(force=True)
        extend_box.fill(PROMPT_PART2)
        time.sleep(1)
        
        # 7. Click Generate on the extend panel
        print("Triggering extension generation...")
        submit_btn = page.locator("button:has-text('arrow_upward'), button[aria-label*='Generate'], button[aria-label*='Submit'], button:has(svg)").last
        submit_btn.click(force=True)
        
        # Wait for Extension to finish
        print("Waiting for Extension to render (35-50s)...")
        time.sleep(35)
        for i in range(30):
            # Check if progress is gone and Insert is visible
            progress = page.locator("text='Your video clip is being generated'")
            if not progress.is_visible():
                btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
                if any(b.is_visible() for b in btns):
                    print(f"Continuous extended video ready in {35 + i*5}s!")
                    break
            time.sleep(5)
            
        page.screenshot(path="output/debug/continuous_extended_ready.png")
        
        # 8. Insert into canvas
        print("Inserting continuous video onto canvas...")
        insert_btn = page.locator("button, [role='button']").filter(has_text="Insert").first
        insert_btn.click(force=True)
        time.sleep(5)
        
        page.screenshot(path="output/debug/continuous_inserted_canvas.png")
        
        # 9. Download the MP4
        videos = page.locator("video").all()
        download_url = None
        for v in reversed(videos):
            src = v.get_attribute("src")
            if src and src.startswith("http"):
                download_url = src
                break
                
        if download_url:
            print(f"Downloading continuous video from {download_url[:70]}...")
            res = page.request.get(download_url)
            if res.status == 200:
                with open(OUT_VIDEO, "wb") as f:
                    f.write(res.body())
                print(f"SUCCESS: Saved {len(res.body())} bytes to {OUT_VIDEO}!")
        else:
            print("Could not find video download URL.")
            
        browser.close()

if __name__ == "__main__":
    main()

