"""
Generates clean, crystal-clear, studio-grade narration for Extended Episode 01.
Uses edge-tts CLI directly to guarantee clean network connections and maximum audio fidelity.
Voice: en-US-EmmaNeural (Warm, clear, comforting preschool educator)
"""
import os
import subprocess
from moviepy import AudioFileClip

OUT_DIR = r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_cinema"
os.makedirs(OUT_DIR, exist_ok=True)

VOICE = "en-US-EmmaNeural"

BEATS = [
    {
        "id": "ep1_beat1_garden_hello",
        "text": "Hello, little explorers! Welcome to Pixieland. Look at Pixy in the sunny garden! Pixy loves the colorful flowers. Can you say Hello? Hello!"
    },
    {
        "id": "ep1_beat2_garden_question",
        "text": "Pixy looks at the wooden garden gate and wonders: 'What is beyond our garden?' Look! In Pixy's backpack, something is shining! Can you say... Look? Look!"
    },
    {
        "id": "ep1_beat3_compass_magic",
        "text": "It is the magical golden compass! It spins, and it glows with bright golden light. Look! It is magic! Can you say Magic? Magic!"
    },
    {
        "id": "ep1_beat4_portal_safety",
        "text": "Wow! A swirling magical portal opens! But remember, little explorers: whenever we explore, we always look carefully and stay safe. Are you ready? Let's go! Go, go, go!"
    },
    {
        "id": "ep1_beat5_leaf_nature_lesson",
        "text": "From high up in the trees, a tiny golden leaf floats down into Pixy's gentle hands. When we explore nature, we are always gentle and kind. Look! Our very first secret clue: a tiny golden leaf! See you on our next adventure. Let's explore!"
    }
]

def main():
    for b in BEATS:
        out_file = os.path.join(OUT_DIR, f"{b['id']}.mp3")
        print(f"Synthesizing {b['id']} via edge-tts CLI...")
        cmd = [
            "edge-tts",
            "--voice", VOICE,
            "--text", b["text"],
            "--write-media", out_file
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            a = AudioFileClip(out_file)
            print(f"SUCCESS: {b['id']}.mp3 | Duration: {a.duration:.2f}s | Size: {os.path.getsize(out_file)} bytes")
            a.close()
        else:
            print(f"FAILED on {b['id']}: {res.stderr}")

if __name__ == "__main__":
    main()

