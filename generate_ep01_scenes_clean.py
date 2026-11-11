"""
Dedicated generator for Episode 01 Scene 3 (The Portal) and Scene 4 (The Golden Leaf Clue).
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/d/1AONoBPseWk9JO13PgZYId3P2l4wNiWBx5B2Pd4ZjDQ8/edit?scene=id.p#scene=id.p"

SCENE3_PROMPT = (
    "Cute 3D Pixar preschool cartoon animation: Pixy in the yellow hoodie stands before a glowing "
    "magical swirling portal of golden and turquoise light energy at the edge of an enchanted forest. "
    "Pixy gasps with wide open delighted eyes and smiles joyfully, breaking into a fun playful run "
    "straight towards the magical glowing portal. Cocomelon preschool style."
)
SCENE3_OUT = r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene3_portal_go.mp4"

SCENE4_PROMPT = (
    "Cute 3D Pixar preschool cartoon animation: Pixy in the bright yellow hoodie is inside a magical enchanted sunlit forest. "
    "A tiny glowing golden leaf floats gently down from the trees into Pixy's open hands. "
    "The golden leaf radiates warm magical sparkles and star dust as Pixy smiles with wonder and joy. Cocomelon preschool style."
)
SCENE4_OUT = r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene4_forest_leaf.mp4"

def generate_single_scene(page, prompt, out_file):
    print(f"\n>>> Generating: {os.path.basename(out_file)} <<<")
    page.keyboard.press("Escape")
    time.sleep(1)
    
    # Ensure AI video panel is opened
    panel = page.locator("[role='textbox'][aria-label*='Describe your video']")
    if not panel.is_visible():
        ai_btn = page.get_by_role("button", name="Generate an AI video clip")
        if ai_btn.is_visible():
            ai_btn.click(force=True)
            time.sleep(2)
            
    # Focus textarea
    textarea = page.locator("[role='textbox'][aria-label*='Describe your video'], [contenteditable='true']").first
    textarea.focus()
    textarea.click(force=True)
    textarea.fill(prompt)
    time.sleep(1)
    
    # Get previous video src count / URLs
    prev_vids = [v.get_attribute("src") for v in page.locator("video").all() if v.get_attribute("src")]
    print(f"Previous video URLs on page: {len(prev_vids)}")
    
    # Click Generate
    gen_btn = page.get_by_role("button", name="Generate", exact=True)
    gen_btn.click(force=True)
    print("Clicked Generate. Waiting minimum 25s for render to start...")
    time.sleep(25)
    
    # Poll for Insert button
    start_time = time.time()
    insert_btn = None
    for i in range(35): # up to 175s
        time.sleep(5)
        # Check if rendering tooltip or progress is done
        progress = page.locator("text='Your video clip is being generated'")
        if not progress.is_visible():
            btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
            for b in btns:
                if b.is_visible():
                    insert_btn = b
                    break
        if insert_btn:
            print(f"New video ready after {int(time.time() - start_time + 25)}s!")
            break
        print(f"Still rendering... ({int(time.time() - start_time + 25)}s)")
        
    if not insert_btn:
        print(f"Failed to find Insert button for {os.path.basename(out_file)}")
        return False
        
    insert_btn.click(force=True)
    time.sleep(5)
    
    # Find the new video URL
    current_vids = [v.get_attribute("src") for v in page.locator("video").all() if v.get_attribute("src")]
    new_url = None
    for src in reversed(current_vids):
        if src.startswith("http") and src not in prev_vids:
            new_url = src
            break
            
    if not new_url and current_vids:
        new_url = current_vids[-1]
        
    print(f"Downloading new video: {new_url[:70]}...")
    res = page.request.get(new_url)
    if res.status == 200:
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        with open(out_file, "wb") as f:
            f.write(res.body())
        print(f"SUCCESS: Saved {len(res.body())} bytes to {out_file}!")
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
        
        # 1. Generate Scene 3 (The Portal)
        generate_single_scene(page, SCENE3_PROMPT, SCENE3_OUT)
        time.sleep(3)
        
        # 2. Generate Scene 4 (The Golden Leaf)
        generate_single_scene(page, SCENE4_PROMPT, SCENE4_OUT)
        
        browser.close()

if __name__ == "__main__":
    main()
