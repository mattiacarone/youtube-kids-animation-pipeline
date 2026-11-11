"""
Batch Generator for Pixieland Episode 01 Animated Video Scenes using Google Vids.
Generates genuine 3D Pixar/Omni animation clips (16:9 Landscape) for the entire episode.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/create"
SCENES_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\scenes"
os.makedirs(SCENES_DIR, exist_ok=True)

SCENES_TO_GENERATE = [
    {
        "id": "vids_scene2_compass",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy, a 5-year-old child explorer in a yellow hoodie, "
            "reaches into a turquoise backpack and holds up a small magical golden compass with both hands. "
            "The compass glows with warm golden volumetric light beams and gentle floating sparkles, illuminating Pixy's excited face. "
            "Cocomelon preschool style, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene2_compass.mp4")
    },
    {
        "id": "vids_scene3_portal",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: In a sunny morning garden between two large ancient oak trees, "
            "a magical swirling golden portal doorway begins to open, radiating warm golden light beams and sparkling star dust. "
            "Gentle magical atmosphere, cinematic landscape 16:9, Cocomelon preschool style."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene3_portal.mp4")
    },
    {
        "id": "vids_scene4_breath_courage",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy in the yellow hoodie stands before the glowing golden portal. "
            "Pixy places one hand gently on the chest, takes a slow calming deep breath, smiles bravely, "
            "and steps gently forward into the warm golden light. Cocomelon preschool style, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene4_breath_courage.mp4")
    },
    {
        "id": "vids_scene5_forest_arrival",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy in the yellow hoodie steps onto a soft mossy forest path "
            "in a magnificent enchanted real-world forest. Pixy looks up in pure wonder and joy at towering green trees "
            "and gentle sunbeams streaming through the leaves. Cocomelon preschool style, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene5_forest_arrival.mp4")
    },
    {
        "id": "vids_scene6_bird_words",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: A cute friendly little forest songbird perches on a mossy tree branch, "
            "chirping happily. Pixy stands nearby, smiling warmly, holding up a bright green leaf and pointing gently to the big tree. "
            "Cocomelon preschool style, educational, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene6_bird_words.mp4")
    },
    {
        "id": "vids_scene7_golden_leaf",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy in the yellow hoodie kneels along the sunny forest path "
            "and picks up a shimmering golden leaf with a mysterious ancient symbol engraved on it. "
            "Pixy holds it up with wonder as the golden compass sparkles in magical resonance. Cocomelon preschool style, 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene7_golden_leaf.mp4")
    },
    {
        "id": "vids_scene8_explorer_journal",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy sits comfortably on a soft mossy log in the forest, "
            "opening the Explorer Journal. Pixy safely places the golden leaf inside and draws a colorful picture of the tree, bird, "
            "and mystery symbol with a crayon, smiling proudly. Cocomelon preschool style, 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene8_explorer_journal.mp4")
    },
    {
        "id": "vids_scene9_outro_farewell",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy looks directly into the camera with a joyful, affectionate preschool smile, "
            "waving both hands goodbye to the young viewers with pure warmth as golden star sparkles float in the air. "
            "Welcoming outro, Cocomelon preschool style, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene9_outro_farewell.mp4")
    }
]

def generate_one_vids_clip(page, prompt, output_file):
    print(f"\n>>> Starting Generation: {os.path.basename(output_file)} <<<")
    if os.path.exists(output_file) and os.path.getsize(output_file) > 500000:
        print(f"File already exists ({os.path.getsize(output_file)} bytes). Skipping.")
        return True
        
    page.goto(VIDS_URL, timeout=45000)
    page.wait_for_timeout(3500)
    
    # Click "Create AI videos"
    create_btn = page.get_by_text("Create AI videos").first
    if create_btn.is_visible():
        create_btn.click(force=True)
        time.sleep(2)
        
    # Focus textarea
    textarea = page.locator("[role='textbox'][aria-label*='Describe your video'], [contenteditable='true']").first
    textarea.focus()
    textarea.click(force=True)
    textarea.fill(prompt)
    time.sleep(1)
    
    # Click Generate
    gen_btn = page.get_by_role("button", name="Generate", exact=True)
    gen_btn.click(force=True)
    print("Submitted prompt to Google Vids. Waiting for rendering...")
    
    # Poll for Insert button
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
        print(f"  Rendering... ({int(time.time() - start_time)}s)")
        
    if not insert_btn:
        print(f"Failed to find Insert button for {os.path.basename(output_file)}")
        return False
        
    insert_btn.click(force=True)
    time.sleep(4)
    
    # Find video src
    videos = page.locator("video").all()
    download_url = None
    for v in reversed(videos):
        src = v.get_attribute("src")
        if src and src.startswith("http"):
            download_url = src
            break
            
    if download_url:
        print(f"Downloading from {download_url[:70]}...")
        res = page.request.get(download_url)
        if res.status == 200:
            with open(output_file, "wb") as f:
                f.write(res.body())
            print(f"SUCCESS: Saved {len(res.body())} bytes to {output_file}!")
            return True
            
    return False

def main():
    print("Connecting to Google Vids session...")
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        for idx, sc in enumerate(SCENES_TO_GENERATE):
            print(f"\n=======================================================")
            print(f"Processing Scene {idx+2}/9: {sc['id']}")
            print(f"=======================================================")
            success = generate_one_vids_clip(page, sc["prompt"], sc["output"])
            if not success:
                print(f"Retrying {sc['id']} once...")
                time.sleep(3)
                generate_one_vids_clip(page, sc["prompt"], sc["output"])
            time.sleep(2)
            
        browser.close()
        print("\nAll Google Vids animated scenes complete!")

if __name__ == "__main__":
    main()
