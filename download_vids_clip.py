"""
Downloads the generated video clip directly from Google Vids using the authenticated session.
"""
import os
import requests
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDEO_URL = (
    "https://contribution-qw.usercontent.google.com/download?"
    "c=CgxiYXJkX3N0b3JhZ2USTBIJdGVtcF9kYXRhGj8KMDBhYWU3MzRjZjQ3ZDdlMjkwMDA2NWRjYzNhMTFhMTMwMDgxMWYzNDM2NTJiN2JhMhILEgcQ6YPytuUFGAE"
    "&filename=video.mp4&opi=108436427&authuser=0"
)

OUT_FILE = r"C:\Users\Mattia\YouTubeKids\assets\clips\vids_penguin_walk.mp4"

def main():
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        
        # Download using browser page request to include all auth cookies
        print(f"Fetching video from {VIDEO_URL[:80]}...")
        response = page.request.get(VIDEO_URL)
        print("Response status:", response.status)
        if response.status == 200:
            body = response.body()
            with open(OUT_FILE, "wb") as f:
                f.write(body)
            print(f"Successfully saved {len(body)} bytes to {OUT_FILE}!")
        else:
            print("Failed to download video, status:", response.status)
            
        browser.close()

if __name__ == "__main__":
    main()
