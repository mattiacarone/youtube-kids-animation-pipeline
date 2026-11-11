"""
Opens the current project in Google Vids where the extension was generating,
inserts the extension clip, and downloads the full continuous video.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
OUT_EXTENDED = r"C:\Users\Mattia\YouTubeKids\assets\clips\pixy_welcoming_part2_compass.mp4"

def main():
    os.makedirs(os.path.dirname(OUT_EXTENDED), exist_ok=True)
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
        
        # Click the most recent Untitled video
        print("Clicking most recent video project...")
        card = page.locator("text=Untitled video").first
        card.click()
        page.wait_for_timeout(6000)
        
        page.screenshot(path="output/debug/vids_reopened_project.png")
        print("Reopened project. Current URL:", page.url)
        
        # Check if AI video panel is open
        ai_btn = page.get_by_role("button", name="Generate an AI video clip")
        if ai_btn.is_visible():
            ai_btn.click(force=True)
            time.sleep(3)
            
        page.screenshot(path="output/debug/vids_extension_finished_check.png")
        
        # Check for Insert button
        btns = page.locator("button, [role='button']").filter(has_text="Insert").all()
        print(f"Found {len(btns)} Insert buttons.")
        for idx, b in enumerate(btns):
            if b.is_visible():
                print(f"Clicking Insert button #{idx}...")
                b.click(force=True)
                time.sleep(3)
                
        page.screenshot(path="output/debug/vids_timeline_with_extension.png")
        
        # Get all video elements on page
        videos = page.locator("video").all()
        print(f"Found {len(videos)} video elements.")
        download_urls = []
        for v in videos:
            src = v.get_attribute("src")
            if src and src.startswith("http") and src not in download_urls:
                download_urls.append(src)
                
        print("Found video download URLs:", len(download_urls))
        for idx, url in enumerate(download_urls):
            target_file = f"C:\\Users\\Mattia\\YouTubeKids\\assets\\clips\\vids_clip_{idx+1}.mp4"
            print(f"Downloading clip {idx+1} to {target_file}...")
            res = page.request.get(url)
            if res.status == 200:
                with open(target_file, "wb") as f:
                    f.write(res.body())
                print(f"Saved {len(res.body())} bytes to {target_file}!")
                
        browser.close()

if __name__ == "__main__":
    main()

