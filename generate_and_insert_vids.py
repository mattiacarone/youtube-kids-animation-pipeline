"""
Full pipeline to generate video in Google Vids and insert it onto the canvas, then extract video URL / download.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/d/1AONoBPseWk9JO13PgZYId3P2l4wNiWBx5B2Pd4ZjDQ8/edit?scene=id.p#scene=id.p"

PROMPT = (
    "Cute 3D Pixar preschool cartoon animation: An adorable chubby baby penguin "
    "waddles happily across sparkling Antarctic snow, flapping its tiny flippers excitedly. "
    "Bright primary colors, sunny pastel turquoise icebergs, Cocomelon preschool style."
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
        
        # Open AI video panel if not open
        panel_header = page.locator("text='AI video clip'")
        if not panel_header.is_visible():
            ai_btn = page.get_by_role("button", name="Generate an AI video clip")
            if ai_btn.is_visible():
                ai_btn.click()
                time.sleep(2)
        
        # Dismiss any popup tooltips
        page.keyboard.press("Escape")
        time.sleep(1)
        
        # Locate textarea
        print("Locating prompt textarea...")
        textarea = page.locator("[role='textbox'][aria-label*='Describe your video'], [contenteditable='true']").first
        textarea.focus()
        textarea.click(force=True)
        textarea.fill(PROMPT)
        time.sleep(1)
        
        # Click Generate button
        print("Clicking Generate button...")
        gen_btn = page.get_by_role("button", name="Generate", exact=True)
        gen_btn.click(force=True)
        print("Generation requested. Waiting for rendering to complete (up to 3 minutes)...")
        
        # Loop check for the Insert button
        start_time = time.time()
        insert_btn = None
        for i in range(36): # 36 * 5s = 180s = 3 minutes
            time.sleep(5)
            # Find insert button
            btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
            for b in btns:
                if b.is_visible():
                    insert_btn = b
                    break
            if insert_btn:
                print(f"Insert button found after {int(time.time() - start_time)}s!")
                break
            print(f"Waiting for video clip generation... ({int(time.time() - start_time)}s)")
            
        page.screenshot(path="output/debug/vids_post_gen.png")
        
        if insert_btn:
            print("Clicking 'Insert' button to save to canvas...")
            insert_btn.click()
            time.sleep(5)
            page.screenshot(path="output/debug/vids_inserted.png")
            print("Saved inserted screenshot at output/debug/vids_inserted.png")
            
            # Check for <video> tags on the page
            video_tags = page.locator("video").all()
            print(f"Found {len(video_tags)} video elements on page.")
            for idx, vt in enumerate(video_tags):
                src = vt.get_attribute("src")
                print(f"Video {idx} src: {src}")
        else:
            print("Insert button did not appear within 3 minutes.")
            
        browser.close()

if __name__ == "__main__":
    main()
