"""Paste your Google AI Studio key once; it is validated and saved to .env."""
import getpass
import os

from google import genai

ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
GITIGNORE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".gitignore")


def main():
    key = getpass.getpass("Paste your Gemini API key (input hidden): ").strip()
    if not key:
        print("No key entered. Nothing saved.")
        return

    print("Validating key with Google AI Studio...")
    try:
        client = genai.Client(api_key=key)
        models = [m.name for m in client.models.list()]
    except Exception as e:
        print(f"[X] Key rejected: {e}")
        return

    veo = [m for m in models if "veo" in m.lower()]
    print(f"[OK] Key valid. {len(models)} models available.")
    if veo:
        print("[OK] Veo video models available:", ", ".join(veo))
    else:
        print("[!] No Veo models visible for this key. Veo requires a billing-enabled (paid tier) project.")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.write(f"GEMINI_API_KEY={key}\n")

    # Make sure the key never ends up in git
    existing = open(GITIGNORE, encoding="utf-8").read() if os.path.exists(GITIGNORE) else ""
    if ".env" not in existing.splitlines():
        with open(GITIGNORE, "a", encoding="utf-8") as f:
            f.write(".env\nyoutube_token.json\nclient_secrets.json\n")

    print(f"Saved to {ENV_PATH}")


if __name__ == "__main__":
    main()

