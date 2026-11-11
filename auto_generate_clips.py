"""
Automated Web Video Generator using saved persistent Google AI session.
Loads scene references, injects motion prompts, and downloads completed clips automatically.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".browser_session")
CLIPS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "clips")

def check_session():
    if not os.path.exists(USER_DATA_DIR) or not os.listdir(USER_DATA_DIR):
        print("\n[!] No active browser session found.")
        print("Please run: python connect_google_session.py to connect your Google AI Pro account once.")
        return False
    return True

if __name__ == "__main__":
    if check_session():
        print(f"Session found at {USER_DATA_DIR}. Ready for automated video generation.")

