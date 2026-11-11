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
        page.goto("https://docs.google.com/videos/u/0/", timeout=30000)
        page.wait_for_timeout(4000)
        links = page.locator("a[href*='/videos/d/']").all()
        print("Recent Google Vids documents:")
        for l in links[:5]:
            print("  ", l.inner_text().replace('\n', ' - '), "->", l.get_attribute("href"))
        browser.close()

if __name__ == "__main__":
    main()
