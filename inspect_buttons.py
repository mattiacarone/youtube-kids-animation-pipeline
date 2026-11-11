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
        
        buttons = page.locator("button, [role='button']").all()
        for b in buttons:
            aria = b.get_attribute("aria-label") or ""
            txt = b.inner_text().strip().replace("\n", " ")
            combined = (aria + " " + txt).lower()
            if any(k in combined for k in ["ingredient", "add", "upload", "animate", "image"]):
                print(f"Button: text='{txt}' | aria='{aria}'")
        browser.close()

if __name__ == "__main__":
    main()
