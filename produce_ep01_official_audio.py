"""
Generates the official preschool child voiceover for Episode 01: "The Magic Compass"
Teaching the 5 roadmap words: hello, look, magic, go, wow + Clue: golden leaf.
"""
import os
import subprocess
import imageio_ffmpeg
from gtts import gTTS
from moviepy import AudioFileClip

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUT_DIR = r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_official"
os.makedirs(OUT_DIR, exist_ok=True)

SCRIPTS = [
    {
        "id": "scene1_hello",
        "text": "Hello! I am Pixy! What is beyond our garden? Can you say hello? Hello!"
    },
    {
        "id": "scene2_look_magic",
        "text": "Look! My golden compass is glowing! It is magic! Can you say magic? Magic!"
    },
    {
        "id": "scene3_wow_go",
        "text": "Wow! A magical swirling portal! Are you ready? Let us go! Go, go, go!"
    },
    {
        "id": "scene4_golden_leaf",
        "text": "Look! A tiny golden leaf! Our first secret clue! See you in the forest! Let us explore!"
    }
]

def generate():
    for item in SCRIPTS:
        raw_mp3 = os.path.join(OUT_DIR, f"{item['id']}_raw.mp3")
        final_mp3 = os.path.join(OUT_DIR, f"{item['id']}.mp3")
        
        print(f"Generating voice for {item['id']}...")
        tts = gTTS(item["text"], lang="en", tld="com")
        tts.save(raw_mp3)
        
        # Pitch shift to cheerful preschool child voice (+24% pitch)
        cmd = [
            FFMPEG, "-y", "-i", raw_mp3,
            "-af", "asetrate=44100*1.22,aresample=44100,atempo=1/1.22",
            final_mp3
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        a = AudioFileClip(final_mp3)
        print(f"Produced {final_mp3}: {a.duration:.2f}s")
        a.close()
        
        if os.path.exists(raw_mp3):
            os.remove(raw_mp3)

if __name__ == "__main__":
    generate()
