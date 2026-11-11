"""
Renders Pixieland Episode 01: "The Magic Compass"
Strictly adhering to the Official 20-Episode Master Roadmap:
- Introduction: Home and forest
- Story: Pixy asks, "What is beyond our garden?" Compass glows and opens a magical portal.
- Vocabulary: hello, look, magic, go, wow
- Clue: A tiny golden leaf
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

SCENES = [
    {
        "id": "scene1_hello",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene1_garden_hello.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_official\scene1_hello.mp3",
        "captions": [
            (0.0, 1.8, "👋 HELLO! 👋", "#FFD700"),
            (1.8, 3.71, "🌸 SAY HELLO! 🌸", "#00E5FF")
        ]
    },
    {
        "id": "scene2_look_magic",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\vids_beat1_compass.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_official\scene2_look_magic.mp3",
        "captions": [
            (0.0, 2.0, "👀 LOOK! 👀", "#FFEB3B"),
            (2.0, 4.05, "✨ MAGIC! ✨", "#E040FB")
        ]
    },
    {
        "id": "scene3_wow_go",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene3_portal_go.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_official\scene3_wow_go.mp3",
        "captions": [
            (0.0, 2.2, "😮 WOW! 😮", "#00E676"),
            (2.2, 4.39, "🚀 LET'S GO! 🚀", "#FF3D00")
        ]
    },
    {
        "id": "scene4_golden_leaf",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene4_forest_leaf.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_official\scene4_golden_leaf.mp3",
        "captions": [
            (0.0, 2.2, "🍃 GOLDEN LEAF! 🍃", "#FFD700"),
            (2.2, 4.31, "⭐ SECRET CLUE! ⭐", "#FFD700")
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
    
    # Place badge in upper third
    x0 = (W - tw) // 2
    y0 = 105
    x1 = x0 + tw
    y1 = y0 + th
    
    # Drop shadow
    draw.rounded_rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], radius=30, fill=(0, 0, 0, 120))
    # Bright candy pill with golden outline
    draw.rounded_rectangle([x0, y0, x1, y1], radius=30, fill=(255, 255, 255, 250), outline=(255, 204, 0, 255), width=7)
    
    # Text with heavy black stroke
    tx = (W - (bbox[2] - bbox[0])) // 2
    ty = y0 + 15
    for dx, dy in [(-3,-3), (3,-3), (-3,3), (3,3), (0,3), (0,-3), (3,0), (-3,0)]:
        draw.text((tx + dx, ty + dy), text, font=font, fill=(0, 0, 0, 255))
    draw.text((tx, ty), text, font=font, fill=text_color)
    
    return np.array(overlay)

def render_scene(cfg):
    audio = AudioFileClip(cfg["audio"])
    dur = audio.duration
    
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
    out_path = r"output\Pixieland_Episode01_The_Magic_Compass.mp4"
    
    print("--- Rendering Pixieland Episode 01: The Magic Compass ---")
    scene_clips = [render_scene(cfg) for cfg in SCENES]
    video_concat = concatenate_videoclips(scene_clips, method="compose")
    total_dur = video_concat.duration
    print(f"Total video duration: {total_dur:.2f} seconds")
    
    # Mix background preschool music
    bgm_path = r"C:\Users\Mattia\YouTubeKids\assets\audio\preschool_bgm.wav"
    if os.path.exists(bgm_path):
        print("Mixing background glockenspiel music...")
        bgm = AudioFileClip(bgm_path)
        if bgm.duration > total_dur:
            bgm = bgm.subclipped(0, total_dur)
        bgm = bgm.with_volume_scaled(0.18)
        mixed_audio = CompositeAudioClip([video_concat.audio, bgm])
        final_video = video_concat.with_audio(mixed_audio)
    else:
        final_video = video_concat
        
    print(f"Exporting to {out_path}...")
    final_video.write_videofile(
        out_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast"
    )
    print(f"\n[DONE] Episode 01 successfully exported to: {out_path}")

if __name__ == "__main__":
    main()
