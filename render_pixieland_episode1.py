"""
Renders the complete Episode 1 of Pixieland for YouTube Kids:
"The Magical Compass & The Penguin"

Structure following the Pixieland Show Bible:
1. Curiosity Hook & Magic Tool: The Golden Compass ("COMPASS") + "Let's explore!"
2. Real-World Arrival & Discovery: Antarctica, Ice ("ICE") and the baby penguin ("PENGUIN")
3. Movement & Physical Mimicry: Action verb ("WADDLE") + "Flap your wings!"
4. Reward & Infinite Loop Hook: "SUPER EXPLORER!" + "Let's explore!" loop back to start.

Features:
- Pure 3D CGI animation clips generated natively via Google Vids
- Crystal-clear preschool speech teaching concrete English words
- Soft acoustic preschool background glockenspiel melody
- Giant bouncy candy-pill caption badges designed for toddler visual focus
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    CompositeVideoClip,
    CompositeAudioClip,
    concatenate_videoclips,
    ImageClip
)

W, H = 720, 1280
FPS = 30
FONT_PATH = r"C:\Windows\Fonts\comicbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"

EPISODE_SCENES = [
    {
        "id": "scene1_compass",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\vids_beat1_compass.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\episode1\ep1_scene1_compass.mp3",
        "captions": [
            (0.0, 2.0, "🧭 COMPASS! 🧭", "#FFD700"),
            (2.0, 3.8, "⭐ C-O-M-P-A-S-S! ⭐", "#FFEB3B"),
            (3.8, 5.62, "✨ LET'S EXPLORE! ✨", "#00E5FF")
        ]
    },
    {
        "id": "scene2_ice_penguin",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\vids_penguin_walk.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\episode1\ep1_scene2_ice_penguin.mp3",
        "captions": [
            (0.0, 2.8, "❄️ ICE! (Cold!) ❄️", "#00E5FF"),
            (2.8, 5.72, "🐧 PENGUIN! 🐧", "#FFD700")
        ]
    },
    {
        "id": "scene3_waddle",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\vids_scene2_waddle.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\episode1\ep1_scene3_waddle.mp3",
        "captions": [
            (0.0, 2.2, "🪽 FLAP YOUR WINGS! 🪽", "#FF4081"),
            (2.2, 4.36, "🐾 WADDLE! WADDLE! 🐾", "#FF9100")
        ]
    },
    {
        "id": "scene4_outro",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\vids_scene3_loop.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\episode1\ep1_scene4_outro.mp3",
        "captions": [
            (0.0, 2.2, "🎉 SUPER EXPLORER! 🎉", "#00E676"),
            (2.2, 4.21, "✨ LET'S EXPLORE! ✨", "#FFD700")
        ]
    }
]

def make_preschool_badge(text, text_color):
    """Creates a high-contrast bouncy bubble caption badge for preschoolers."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font = ImageFont.truetype(FONT_PATH, 50)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0] + 80
    th = bbox[3] - bbox[1] + 50
    
    # Place badge in upper third (high visibility on mobile Shorts)
    x0 = (W - tw) // 2
    y0 = 100
    x1 = x0 + tw
    y1 = y0 + th
    
    # Drop shadow
    draw.rounded_rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], radius=30, fill=(0, 0, 0, 120))
    # Bright candy pill with golden outline
    draw.rounded_rectangle([x0, y0, x1, y1], radius=30, fill=(255, 255, 255, 250), outline=(255, 204, 0, 255), width=7)
    
    # Text with heavy black outline for readability
    tx = (W - (bbox[2] - bbox[0])) // 2
    ty = y0 + 15
    for dx, dy in [(-3,-3), (3,-3), (-3,3), (3,3), (0,3), (0,-3), (3,0), (-3,0)]:
        draw.text((tx + dx, ty + dy), text, font=font, fill=(0, 0, 0, 255))
    draw.text((tx, ty), text, font=font, fill=text_color)
    
    return np.array(overlay)

def render_scene(cfg):
    audio = AudioFileClip(cfg["audio"])
    dur = audio.duration
    
    # Load Google Vids animated clip
    vclip = VideoFileClip(cfg["video"])
    if vclip.duration > dur:
        vclip = vclip.subclipped(0, dur)
    else:
        dur = vclip.duration
        
    layers = [vclip]
    for start_t, end_t, text, color in cfg["captions"]:
        c_dur = min(end_t, dur) - start_t
        if c_dur <= 0:
            continue
        badge_np = make_preschool_badge(text, color)
        badge_clip = ImageClip(badge_np, duration=c_dur).with_start(start_t)
        layers.append(badge_clip)
        
    return CompositeVideoClip(layers, size=(W, H)).with_duration(dur).with_audio(audio)

def main():
    os.makedirs("output", exist_ok=True)
    out_path = r"output\Pixieland_Episode1_The_Magical_Compass.mp4"
    
    print("--- Assembling Pixieland Episode 1 ---")
    scene_clips = [render_scene(cfg) for cfg in EPISODE_SCENES]
    video_concat = concatenate_videoclips(scene_clips, method="compose")
    total_dur = video_concat.duration
    print(f"Total video duration: {total_dur:.2f} seconds")
    
    # Add gentle background glockenspiel BGM
    bgm_path = r"C:\Users\Mattia\YouTubeKids\assets\audio\preschool_bgm.wav"
    if os.path.exists(bgm_path):
        print("Mixing preschool background music...")
        bgm = AudioFileClip(bgm_path)
        if bgm.duration > total_dur:
            bgm = bgm.subclipped(0, total_dur)
        bgm = bgm.with_volume_scaled(0.18)
        
        # Mix speech + bgm
        mixed_audio = CompositeAudioClip([video_concat.audio, bgm])
        final_video = video_concat.with_audio(mixed_audio)
    else:
        final_video = video_concat
        
    print(f"Exporting Episode 1 to {out_path}...")
    final_video.write_videofile(
        out_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast"
    )
    print(f"\n[SUCCESS] Pixieland Episode 1 exported to: {out_path}")

if __name__ == "__main__":
    main()
