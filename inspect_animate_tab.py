import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
URL = "https://docs.google.com/videos/d/1AONoBPseWk9JO13PgZYId3P2l4wNiWBx5B2Pd4ZjDQ8/edit?scene=id.p#scene=id.p"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(URL, timeout=45000)
        page.wait_for_timeout(4000)
        
        # Click the Animate tab in AI video panel
        print("Clicking 'Animate' tab...")
        animate_tab = page.locator("text=Animate").first
        if animate_tab.is_visible():
            animate_tab.click()
            time.sleep(2)
            
        page.screenshot(path="output/debug/vids_animate_tab.png")
        print("Captured vids_animate_tab.png")
        browser.close()

if __name__ == "__main__":
    main()
