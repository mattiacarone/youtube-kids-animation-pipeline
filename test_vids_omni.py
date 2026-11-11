import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/create"

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
        
        # Click "Create AI videos"
        print("Clicking 'Create AI videos'...")
        create_btn = page.get_by_text("Create AI videos").first
        if create_btn.is_visible():
            create_btn.click()
            time.sleep(2)
            
        page.screenshot(path="output/debug/vids_ai_panel.png")
        print("Screenshot saved to output/debug/vids_ai_panel.png")
        
        # Find all textboxes
        textboxes = page.locator("[role='textbox'], [contenteditable='true'], textarea").all()
        print(f"Found {len(textboxes)} textboxes:")
        for t in textboxes:
            print("  Box:", t.get_attribute("aria-label"), "| placeholder:", t.get_attribute("placeholder"))
            
        browser.close()

if __name__ == "__main__":
    main()
