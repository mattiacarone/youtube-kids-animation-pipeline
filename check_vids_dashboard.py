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
        page.wait_for_timeout(5000)
        page.screenshot(path="output/debug/vids_home_recent.png")
        print("Page title:", page.title())
        
        # Look for any recent video links
        links = page.locator("a[href*='/videos/d/']").all()
        print("Found video links:", len(links))
        for l in links:
            href = l.get_attribute("href")
            text = l.inner_text().replace("\n", " ")
            print(f"Video: {text} -> {href}")
            
        browser.close()

if __name__ == "__main__":
    main()
