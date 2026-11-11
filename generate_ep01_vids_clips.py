"""
Batch video generation for Pixieland Episode 01: "The Magic Compass"
Generates Scene 1 (Garden Hello), Scene 3 (Magical Portal Go), and Scene 4 (Enchanted Forest Leaf Clue).
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/d/1AONoBPseWk9JO13PgZYId3P2l4wNiWBx5B2Pd4ZjDQ8/edit?scene=id.p#scene=id.p"

CLIPS_TO_GENERATE = [
    {
        "id": "ep01_scene1_garden_hello",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy, an adorable 5-year-old child explorer "
            "with messy brown hair and big expressive bright eyes, wearing a bright yellow hoodie, "
            "stands in a sunny flower garden. Pixy waves enthusiastically at the camera with a joyful open-mouth smile "
            "saying hello, looking at a wooden garden gate with bright flowers. Cocomelon preschool style."
        ),
        "output": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene1_garden_hello.mp4"
    },
    {
        "id": "ep01_scene3_portal_go",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy in the yellow hoodie stands before a magical glowing "
            "swirling portal of golden and turquoise light at the edge of an enchanted forest. "
            "Pixy has a wide delighted gasp of pure awe, smiling enthusiastically at the camera and breaking into a fun run "
            "towards the glowing portal. Cocomelon preschool style."
        ),
        "output": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene3_portal_go.mp4"
    },
    {
        "id": "ep01_scene4_forest_leaf",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy in the yellow hoodie is in an enchanted sunlit green forest. "
            "A tiny glowing golden leaf floats gently down from the treetops into Pixy's open hands. "
            "The golden leaf radiates warm magical sparkles and star dust as Pixy smiles with wonder and joy. Cocomelon preschool style."
        ),
        "output": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene4_forest_leaf.mp4"
    }
]

def generate_clip(page, prompt, output_path):
    print(f"\n=======================================================")
    print(f"Generating clip: {os.path.basename(output_path)}")
    print(f"=======================================================")
    
    if os.path.exists(output_path) and os.path.getsize(output_path) > 500000:
        print(f"Clip already exists ({os.path.getsize(output_path)} bytes), skipping generation.")
        return True

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
    print("Submitted prompt to Google Vids. Waiting for rendering to complete...")
    
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
        print(f"Error: Insert button did not appear for {os.path.basename(output_path)}.")
        return False
        
    insert_btn.click(force=True)
    time.sleep(4)
    
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
            print(f"SUCCESS: Saved {len(res.body())} bytes to {output_path}!")
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
        
        for clip_cfg in CLIPS_TO_GENERATE:
            ok = generate_clip(page, clip_cfg["prompt"], clip_cfg["output"])
            if not ok:
                print(f"Failed on {clip_cfg['id']}, stopping batch.")
                break
            time.sleep(3)
            
        browser.close()

if __name__ == "__main__":
    main()
