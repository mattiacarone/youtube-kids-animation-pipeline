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
        
        # Click the AI video button
        print("Clicking 'Generate an AI video clip'...")
        ai_btn = page.get_by_role("button", name="Generate an AI video clip")
        if ai_btn.is_visible():
            ai_btn.click()
            time.sleep(3)
        
        page.screenshot(path="output/debug/vids_ai_panel_state.png")
        print("Captured vids_ai_panel_state.png")
        
        # Check text in the side panel
        texts = page.locator("div[role='dialog'], [aria-label*='AI video'], .appsSketchySideSheetContainer").inner_text()
        print("Panel text:\n", texts)
        
        browser.close()

if __name__ == "__main__":
    main()
