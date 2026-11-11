import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/create"
OUT_TEST = r"C:\Users\Mattia\YouTubeKids\assets\clips\test_landscape_vids.mp4"

PROMPT = (
    "Cute 3D Pixar preschool cartoon animation: Pixy, a 5-year-old child explorer in a bright yellow hoodie, "
    "waves warmly hello with both hands in a sunny morning garden with colorful blooming flowers and a fluttering butterfly. "
    "Warm golden morning sunlight, cinematic composition, Cocomelon preschool style."
)

def main():
    print("Launching Google Vids for Landscape AI animation test...")
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
        
        # Notice: DO NOT click Portrait! Google Vids defaults to Landscape!
        print("Opening 'Create AI videos'...")
        create_btn = page.get_by_text("Create AI videos").first
        if create_btn.is_visible():
            create_btn.click()
            time.sleep(2)
            
        # Fill prompt
        print("Filling prompt...")
        textarea = page.locator("[role='textbox'][aria-label*='Describe your video'], [contenteditable='true']").first
        textarea.focus()
        textarea.click(force=True)
        textarea.fill(PROMPT)
        time.sleep(1)
        
        # Click Generate
        print("Clicking Generate...")
        gen_btn = page.get_by_role("button", name="Generate", exact=True)
        gen_btn.click(force=True)
        
        # Poll for Insert button
        print("Waiting for generation to finish...")
        start_time = time.time()
        insert_btn = None
        for i in range(35): # up to 175s
            time.sleep(5)
            btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
            for b in btns:
                if b.is_visible():
                    insert_btn = b
                    break
            if insert_btn:
                print(f"Generated successfully in {int(time.time() - start_time)}s!")
                break
            print(f"Rendering AI animation... ({int(time.time() - start_time)}s)")
            
        if not insert_btn:
            print("Failed to find Insert button.")
            page.screenshot(path="output/debug/vids_fail.png")
            browser.close()
            return
            
        insert_btn.click(force=True)
        time.sleep(4)
        
        # Get video src
        videos = page.locator("video").all()
        download_url = None
        for v in reversed(videos):
            src = v.get_attribute("src")
            if src and src.startswith("http"):
                download_url = src
                break
                
        print("Video URL:", download_url)
        if download_url:
            res = page.request.get(download_url)
            if res.status == 200:
                with open(OUT_TEST, "wb") as f:
                    f.write(res.body())
                print(f"SAVED {len(res.body())} bytes to {OUT_TEST}!")
                
        browser.close()

if __name__ == "__main__":
    main()
