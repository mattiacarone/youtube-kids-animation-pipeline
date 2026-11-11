import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto("https://docs.google.com/videos/u/0/", timeout=45000)
        page.wait_for_timeout(4000)
        
        # Click the first Untitled video card
        print("Clicking first recent video card...")
        card = page.locator("text=Untitled video").first
        card.click()
        page.wait_for_timeout(6000)
        
        # Check current URL
        print("Current URL:", page.url)
        page.screenshot(path="output/debug/vids_opened_video.png")
        
        # Check if AI video button or panel is open
        ai_video_btn = page.get_by_text("AI video")
        if ai_video_btn.is_visible():
            print("Clicking AI video tab on the right...")
            ai_video_btn.click()
            page.wait_for_timeout(3000)
            page.screenshot(path="output/debug/vids_opened_ai_panel.png")
            
        browser.close()

if __name__ == "__main__":
    main()
