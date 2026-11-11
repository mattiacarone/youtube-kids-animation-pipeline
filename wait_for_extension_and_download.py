"""
Reopens the active project, waits for the extension to complete (until Cancel disappears),
clicks Insert, and downloads the continuous video.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_HOME = "https://docs.google.com/videos/u/0/"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.goto(VIDS_HOME, timeout=45000)
        page.wait_for_timeout(4000)
        
        # Click the most recent video card
        print("Clicking most recent video card...")
        card = page.locator("text=Untitled video").first
        card.click()
        page.wait_for_timeout(6000)
        
        # Open AI video panel
        ai_btn = page.get_by_role("button", name="Generate an AI video clip")
        if ai_btn.is_visible():
            ai_btn.click(force=True)
            time.sleep(3)
            
        page.screenshot(path="output/debug/wait_ext_state1.png")
        
        # Check if Cancel button is visible (meaning still generating)
        cancel_btn = page.locator("text=Cancel")
        print("Checking if generation is still active...")
        start_wait = time.time()
        while cancel_btn.is_visible():
            elapsed = int(time.time() - start_wait)
            print(f"Still generating extension... ({elapsed}s)")
            time.sleep(5)
            if elapsed > 120:
                print("Wait timed out after 120s.")
                break
                
        page.screenshot(path="output/debug/wait_ext_state2.png")
        
        # Click Insert for the extension
        print("Looking for Insert button for the extension...")
        insert_btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
        print(f"Found {len(insert_btns)} Insert buttons.")
        for idx, btn in enumerate(insert_btns):
            if btn.is_visible():
                print(f"Clicking Insert button #{idx}...")
                btn.click(force=True)
                time.sleep(4)
                
        page.screenshot(path="output/debug/wait_ext_final_timeline.png")
        
        # Download all videos
        videos = page.locator("video").all()
        print(f"Found {len(videos)} video elements.")
        download_urls = []
        for v in videos:
            src = v.get_attribute("src")
            if src and src.startswith("http") and src not in download_urls:
                download_urls.append(src)
                
        print(f"Extracted {len(download_urls)} video URLs.")
        for idx, url in enumerate(download_urls):
            out_file = f"C:\\Users\\Mattia\\YouTubeKids\\assets\\clips\\continuous_ext_{idx+1}.mp4"
            print(f"Downloading clip {idx+1} -> {out_file}...")
            res = page.request.get(url)
            if res.status == 200:
                with open(out_file, "wb") as f:
                    f.write(res.body())
                print(f"Saved {len(res.body())} bytes to {out_file}!")
                
        browser.close()

if __name__ == "__main__":
    main()

