"""
Automated Google Session Connect script.
Uses Playwright bundled Chromium to avoid Windows Chrome locks.
Keeps running until you click 'Done' or close the browser window.
"""
import os
import sys
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".browser_session")

def main():
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    print("Launching Chromium for Google Login...")
    
    with sync_playwright() as p:
        # Use bundled Chromium rather than channel='chrome' to prevent profile conflicts
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 850},
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        page.goto("https://accounts.google.com/ServiceLogin?continue=https://labs.google/fx/tools/videofx")
        
        print("\n" + "="*60)
        print("Chromium window is OPEN on your screen.")
        print("Please sign into your Google account.")
        print("When you are finished and reach the page, simply CLOSE the browser window.")
        print("="*60 + "\n")
        
        # Wait until the user closes the page/browser window
        while context.pages:
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                break
                
        context.close()
        print("Session cookies successfully saved to .browser_session!")

if __name__ == "__main__":
    main()
