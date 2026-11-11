"""
Generates the Compass Introduction clip in Google Vids and downloads the MP4.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/d/1AONoBPseWk9JO13PgZYId3P2l4wNiWBx5B2Pd4ZjDQ8/edit?scene=id.p#scene=id.p"

COMPASS_PROMPT = (
    "Cute 3D Pixar preschool cartoon animation: Pixi, an adorable 5-year-old child explorer "
    "wearing a bright yellow hoodie, holds up a magical glowing golden compass with both hands. "
    "The golden compass spins and emits warm glowing golden light beams and floating magical star sparkles. "
    "Pixi looks at the camera with big joyful expressive eyes and a delighted gasp. Cocomelon preschool style."
)

COMPASS_OUT = r"C:\Users\Mattia\YouTubeKids\assets\clips\vids_beat1_compass.mp4"

def generate_clip(page, prompt, output_path):
    print(f"\n--- Generating clip: {os.path.basename(output_path)} ---")
    page.keyboard.press("Escape")
    time.sleep(1)
    
    # Open AI video panel if needed
    panel = page.locator("[role='textbox'][aria-label*='Describe your video']")
    if not panel.is_visible():
        ai_btn = page.get_by_role("button", name="Generate an AI video clip")
        if ai_btn.is_visible():
            ai_btn.click(force=True)
            time.sleep(2)
        
    # Fill prompt
    textarea = page.locator("[role='textbox'][aria-label*='Describe your video'], [contenteditable='true']").first
    textarea.focus()
    textarea.click(force=True)
    textarea.fill(prompt)
    time.sleep(1)
    
    # Click Generate
    gen_btn = page.get_by_role("button", name="Generate", exact=True)
    gen_btn.click(force=True)
    print("Submitted Compass prompt to Google Vids. Waiting for rendering to complete...")
    
    # Poll for Insert button
    start_time = time.time()
    insert_btn = None
    for _ in range(40): # up to 200s
        time.sleep(5)
        btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
        for b in btns:
            if b.is_visible():
                insert_btn = b
                break
        if insert_btn:
            print(f"Insert button ready after {int(time.time() - start_time)}s!")
            break
        print(f"Rendering in progress... ({int(time.time() - start_time)}s)")
        
    if not insert_btn:
        print("Error: Insert button did not appear in time.")
        page.screenshot(path="output/debug/compass_timeout.png")
        return False
        
    # Get video element src
    insert_btn.click(force=True)
    time.sleep(4)
    page.screenshot(path=f"output/debug/inserted_{os.path.basename(output_path)}.png")
    
    videos = page.locator("video").all()
    download_url = None
    for v in reversed(videos):
        src = v.get_attribute("src")
        if src and ("contribution-qw" in src or "blob:" in src or "http" in src):
            download_url = src
            break
            
    print("Found video src:", download_url)
    if download_url and download_url.startswith("http"):
        res = page.request.get(download_url)
        if res.status == 200:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(res.body())
            print(f"Saved {len(res.body())} bytes to {output_path}!")
            return True
    return False

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
        
        generate_clip(page, COMPASS_PROMPT, COMPASS_OUT)
        
        browser.close()

if __name__ == "__main__":
    main()

