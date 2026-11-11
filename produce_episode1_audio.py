"""
Generates clean preschool voiceover using gTTS and applies ffmpeg pitch shift to achieve a child's voice.
"""
import os
import subprocess
import imageio_ffmpeg
from gtts import gTTS
from moviepy import AudioFileClip

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
OUT_DIR = r"C:\Users\Mattia\YouTubeKids\assets\audio\episode1"
os.makedirs(OUT_DIR, exist_ok=True)

SCRIPTS = [
    {
        "id": "ep1_scene1_compass",
        "text": "Look! My magical golden compass! Can you say compass? Compass! Where are we going today? Let us explore!"
    },
    {
        "id": "ep1_scene2_ice_penguin",
        "text": "Brrr! Look at the ice! So cold! And look, an adorable baby penguin! Can you say penguin? Penguin!"
    },
    {
        "id": "ep1_scene3_waddle",
        "text": "Can you waddle like a penguin? Flap your wings! Waddle, waddle, waddle! Look at you go!"
    },
    {
        "id": "ep1_scene4_outro",
        "text": "Yay! You did it! You are a super explorer! See you on our next adventure! Let us explore!"
    }
]

def generate_voice():
    for item in SCRIPTS:
        raw_mp3 = os.path.join(OUT_DIR, f"{item['id']}_raw.mp3")
        final_mp3 = os.path.join(OUT_DIR, f"{item['id']}.mp3")
        
        print(f"Generating gTTS for {item['id']}...")
        tts = gTTS(item["text"], lang="en", tld="com")
        tts.save(raw_mp3)
        
        # Pitch shift by +25% using asetrate and atempo
        # asetrate=44100*1.24 -> raises pitch to cute preschool child voice
        # atempo=1/1.24 -> keeps natural speaking pace
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
    generate_voice()
