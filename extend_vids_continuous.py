"""
Inspects the current project and triggers the extension to completion.
"""
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
PROJECT_URL = "https://docs.google.com/videos/d/1fCRbNpthUydrLZWdaYMrQrI0alfx8W1le0slD0JQmoo/edit?scene=id.p#scene=id.p"

EXTEND_PROMPT = (
    "Pixy smiles warmly, reaches into his pocket and holds up the magical golden compass with both hands. "
    "The golden compass spins and emits warm glowing light beams and gentle star sparkles. "
    "Pixy smiles happily at the camera. Seamless continuous camera, warm cozy room, no cuts."
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
        page.goto(PROJECT_URL, timeout=45000)
        page.wait_for_timeout(4000)
        
        # Click on the video in the timeline or canvas to select it
        print("Selecting video on canvas...")
        canvas_video = page.locator("div[role='img'], canvas, video").first
        if canvas_video.is_visible():
            canvas_video.click()
            time.sleep(1)
            
        # Click AI video panel
        print("Opening AI video panel...")
        ai_btn = page.get_by_role("button", name="Generate an AI video clip")
        if ai_btn.is_visible():
            ai_btn.click(force=True)
            time.sleep(2)
            
        page.screenshot(path="output/debug/extend_panel_check.png")
        
        # Check Extend tab
        extend_tab = page.locator("text=Extend").all()
        print(f"Found {len(extend_tab)} Extend elements.")
        for et in extend_tab:
            if et.is_visible():
                print("Clicking Extend tab...")
                et.click(force=True)
                time.sleep(2)
                break
                
        page.screenshot(path="output/debug/extend_tab_active.png")
        
        # Look for textarea in Extend panel
        textareas = page.locator("[role='textbox'], [contenteditable='true']").all()
        print(f"Found {len(textareas)} textboxes.")
        for ta in textareas:
            if ta.is_visible():
                print("Filling extend prompt...")
                ta.focus()
                ta.fill(EXTEND_PROMPT)
                time.sleep(1)
                
                # Click Submit / Arrow
                submit_btn = page.locator("button:has-text('arrow_upward'), button[aria-label*='Generate'], button[aria-label*='Submit'], button:has(svg)").last
                submit_btn.click(force=True)
                print("Submitted extension! Waiting 60s for completion...")
                
                # Wait until done
                for i in range(20):
                    time.sleep(5)
                    progress = page.locator("text='%'").all()
                    if not progress:
                        btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
                        if any(b.is_visible() for b in btns):
                            print(f"Extension finished after {5 + i*5}s!")
                            break
                    print(f"Extension rendering... ({5 + i*5}s)")
                break
                
        page.screenshot(path="output/debug/extend_completed.png")
        browser.close()

if __name__ == "__main__":
    main()

