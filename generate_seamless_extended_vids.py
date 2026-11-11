"""
Generates a truly seamless, extended continuous video in Google Vids.
Waits fully (up to 120s) for the extension to complete and inserts it to the timeline.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/create"

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
        
        # Wait for Part 1 to finish (up to 90s)
        print("Waiting for Part 1 rendering...")
        start_t = time.time()
        for i in range(25):
            time.sleep(5)
            btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
            if any(b.is_visible() for b in btns):
                print(f"Part 1 ready in {int(time.time() - start_t)}s!")
                break
                
        # Insert Part 1 to timeline
        print("Inserting Part 1 into canvas...")
        insert_btn = page.locator("button, [role='button']").filter(has_text="Insert").first
        insert_btn.click(force=True)
        time.sleep(4)
        
        # 5. Click Extend
        print("Clicking Extend button...")
        extend_btn = page.locator("button, [role='button']").filter(has_text="Extend").first
        extend_btn.click(force=True)
        time.sleep(2)
        
        # 6. Fill Extend Prompt (Part 2)
        print("Filling Extend prompt (Part 2)...")
        extend_box = page.locator("[role='textbox'][aria-label*='Create a video and describe'], [role='textbox'][aria-label*='Describe'], [contenteditable='true']").first
        extend_box.focus()
        extend_box.click(force=True)
        extend_box.fill(PROMPT_PART2)
        time.sleep(1)
        
        # 7. Click Generate for Extension
        print("Submitting extension generation...")
        submit_btn = page.locator("button:has-text('arrow_upward'), button[aria-label*='Generate'], button[aria-label*='Submit'], button:has(svg)").last
        submit_btn.click(force=True)
        
        # 8. Wait for Extension to reach 100% (up to 120s)
        print("Waiting for Extension to reach 100%...")
        start_ext = time.time()
        ext_insert_btn = None
        for i in range(30): # 30 * 5s = 150s
            time.sleep(5)
            # Check if percentage progress is still present
            progress = page.locator("text='%'").all()
            elapsed = int(time.time() - start_ext)
            print(f"Extension rendering... ({elapsed}s, active progress elements: {len(progress)})")
            
            # Check for newly enabled Insert button
            if not progress:
                insert_candidates = page.locator("button, [role='button']").filter(has_text="Insert").all()
                for b in insert_candidates:
                    if b.is_visible():
                        ext_insert_btn = b
                        break
                if ext_insert_btn:
                    print(f"Extension completed in {elapsed}s!")
                    break
                    
        page.screenshot(path="output/debug/extend_100_percent.png")
        
        if ext_insert_btn:
            print("Clicking Insert for Extension...")
            ext_insert_btn.click(force=True)
            time.sleep(5)
            page.screenshot(path="output/debug/extend_inserted_timeline.png")
            
        # 9. Check video elements and download all clips
        videos = page.locator("video").all()
        print(f"Found {len(videos)} video elements on page.")
        download_urls = []
        for v in videos:
            src = v.get_attribute("src")
            if src and src.startswith("http") and src not in download_urls:
                download_urls.append(src)
                
        print(f"Extracted {len(download_urls)} video URLs.")
        for idx, url in enumerate(download_urls):
            out_file = f"C:\\Users\\Mattia\\YouTubeKids\\assets\\clips\\seamless_clip_{idx+1}.mp4"
            print(f"Downloading clip {idx+1} -> {out_file}...")
            res = page.request.get(url)
            if res.status == 200:
                with open(out_file, "wb") as f:
                    f.write(res.body())
                print(f"Saved {len(res.body())} bytes to {out_file}!")
                
        browser.close()

if __name__ == "__main__":
    main()

