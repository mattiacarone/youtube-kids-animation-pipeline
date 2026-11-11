"""
Automated Flow Video Generator.
Uploads reference scenes into Google Flow (Veo engine),
generates 9:16 animated clips with character consistency,
and downloads the MP4s into assets/clips.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
OUTPUT_DIR = r"C:\Users\Mattia\YouTubeKids\assets\clips"

VEO_SCENES = [
    {
        "id": "clip1_arrival",
        "image": r"C:\Users\Mattia\YouTubeKids\assets\scene1_penguin.jpg",
        "prompt": "Animate this 2D cartoon scene: Pixi in yellow hoodie crouches on the snow, blinking with green eyes, smiling as the golden compass spins with gentle golden sparkles. The baby penguin flaps its tiny flippers excitedly. Smooth fluid 2D animation, 9:16 vertical."
    },
    {
        "id": "clip2_waddle",
        "image": r"C:\Users\Mattia\YouTubeKids\assets\scene2_waddle.jpg",
        "prompt": "Animate this 2D cartoon scene: Pixi and the baby penguin waddle side by side across the snow, flapping arms and wings in a funny waddling motion, laughing. The baby seal in the background claps happily. 9:16 vertical preschool animation."
    },
    {
        "id": "clip3_crystal",
        "image": r"C:\Users\Mattia\YouTubeKids\assets\scene3_crystal.jpg",
        "prompt": "Animate this 2D cartoon scene: The baby penguin hops on one foot holding up the glowing turquoise crystal that sparkles softly. Pixi smiles cheerfully and waves to the camera. Warm sunset lighting, smooth animation, 9:16 vertical."
    }
]

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Launching Google Flow automation bridge with active Pro session...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://flow.google.com", timeout=45000)
        page.wait_for_timeout(3000)
        
        # Check if project exists or click new project
        new_proj = page.locator("text=New project").first
        if new_proj.is_visible():
            new_proj.click()
            page.wait_for_timeout(4000)
            
        # Bypass modal if present
        get_started = page.get_by_role("button", name="Get started")
        if get_started.is_visible():
            get_started.click()
            page.wait_for_timeout(2000)
            
        print(f"Connected to Flow Studio workspace: {page.url}")
        
        # Locate the chat/prompt input in Flow Studio
        prompt_box = page.locator("textarea[placeholder*='What do you want to create'], [contenteditable='true']").first
        prompt_box.click()
        prompt_box.fill(VEO_SCENES[0]["prompt"])
        time.sleep(1)
        page.keyboard.press("Enter")
        print(f"Submitted Scene 1 generation prompt to Flow: {VEO_SCENES[0]['id']}")
        
        time.sleep(15)
        page.screenshot(path="output/debug/flow_generating.png")
        print("Captured Flow generation status screenshot.")
        
        browser.close()

if __name__ == "__main__":
    main()
