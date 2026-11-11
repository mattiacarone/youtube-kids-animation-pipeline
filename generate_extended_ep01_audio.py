"""
Generates the warm, crystal-clear preschool narration for the extended Episode 01.
Voice: en-US-EmmaNeural (Warm, articulate, comforting preschool educator)
"""
import os
import asyncio
import edge_tts
from moviepy import AudioFileClip

OUT_DIR = r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_extended"
os.makedirs(OUT_DIR, exist_ok=True)

VOICE = "en-US-EmmaNeural"

BEATS = [
    {
        "id": "beat1_garden_hello",
        "text": "Hello, little explorers! Welcome to Pixieland. This is Pixy. Pixy loves to look at the flowers in the garden. Can you say... Hello? Hello!"
    },
    {
        "id": "beat2_garden_look",
        "text": "Pixy looks at the wooden garden gate and wonders: 'What is beyond our garden?' Look! In Pixy's hands, something is shining! Can you say... Look? Look!"
    },
    {
        "id": "beat3_compass_magic",
        "text": "It is the golden compass! It spins, and it glows with warm golden light. It is magic! Can you say... Magic? Magic!"
    },
    {
        "id": "beat4_portal_go",
        "text": "A shimmering portal opens like a doorway of light. But remember, little explorers: whenever we go on an adventure, we always look carefully and stay safe. Are you ready? Let us... go! Go, go, go!"
    },
    {
        "id": "beat5_forest_wow",
        "text": "Pixy steps through into the enchanted forest. Look at the tall green trees and the soft sunlight. Wow! Can you say... Wow? Wow!"
    },
    {
        "id": "beat6_leaf_lesson",
        "text": "From high up in the branches, a tiny golden leaf floats down. Pixy catches it with gentle, loving hands. When we explore nature, we are always gentle and kind. We found our very first secret clue: a tiny golden leaf! See you on our next adventure. Let us explore!"
    }
]

async def generate():
    for b in BEATS:
        out_file = os.path.join(OUT_DIR, f"{b['id']}.mp3")
        print(f"Generating {b['id']} with {VOICE}...")
        # Rate slightly relaxed for preschool clarity (-5%)
        comm = edge_tts.Communicate(b["text"], VOICE)
        await comm.save(out_file)
        await asyncio.sleep(1.0)
        
        a = AudioFileClip(out_file)
        print(f"Saved {b['id']}.mp3: duration={a.duration:.2f}s")
        a.close()

def main():
    asyncio.run(generate())

if __name__ == "__main__":
    main()
