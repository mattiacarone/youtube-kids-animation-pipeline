"""
Generates the crystal-clear preschool educational voiceover for Episode 1 using edge-tts.
Follows the Pixieland Show Bible structure:
- Curiosity & Compass
- Real World & Concrete Words (Compass, Ice, Penguin, Waddle)
- Call-and-response repetition
- Celebration & Catchphrase loop ("Let's explore!")
"""
import os
import asyncio
import edge_tts

VOICE = "en-US-AnaNeural" # Child voice: warm, friendly, clear
OUTPUT_DIR = r"C:\Users\Mattia\YouTubeKids\assets\audio\episode1"

SCENES_AUDIO = [
    {
        "file": "ep1_scene1_compass.mp3",
        "text": "Look! My magical golden compass! Can you say compass? Compass! Where are we going? Let's explore!"
    },
    {
        "file": "ep1_scene2_ice_penguin.mp3",
        "text": "Brrr! Look at the ice! So cold! And look... a cute baby penguin! Say penguin!"
    },
    {
        "file": "ep1_scene3_waddle.mp3",
        "text": "Can you waddle like a penguin? Flap your wings! Waddle, waddle, waddle! Good job!"
    },
    {
        "file": "ep1_scene4_outro.mp3",
        "text": "Yay! You did it! You're a super explorer! See you on our next adventure... Let's explore!"
    }
]

async def generate():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for item in SCENES_AUDIO:
        out_path = os.path.join(OUTPUT_DIR, item["file"])
        print(f"Generating voiceover: {item['file']}...")
        # Slower rate for clear preschool comprehension (+0% or -5%)
        communicate = edge_tts.Communicate(item["text"], VOICE, rate="-4%", pitch="+2Hz")
        await communicate.save(out_path)
        print(f"Saved: {out_path}")

def main():
    asyncio.run(generate())

if __name__ == "__main__":
    main()
