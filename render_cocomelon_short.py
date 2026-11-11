"""
Renders the high-energy, 18-second Cocomelon-style Short for YouTube Kids.
Uses 3D character assets, syncopated cuts, dynamic pop-in bouncy captions,
and seamless loop design.
"""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips

W, H = 1080, 1920
FPS = 30
FONT_PATH = r"C:\Windows\Fonts\comicbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"

SCENES = [
    {
        "id": "scene1_hook",
        "image": "assets/cocomelon_style_pixi.png",
        "audio": "assets/audio/cocomelon_scene1.mp3",
        "captions": [
            (0.0, 2.2, "❄️ WHOA! BRRR! ❄️", "#FFD700"),
            (2.2, 5.2, "🐧 BABY PENGUIN! 🐧", "#00E5FF")
        ]
    },
    {
        "id": "scene2_waddle",
        "image": "assets/cocomelon_scene2_waddle.png",
        "audio": "assets/audio/cocomelon_scene2.mp3",
        "captions": [
            (0.0, 3.5, "🐾 HE WADDLES! 🐾", "#FF4081"),
            (3.5, 7.3, "🐧 CAN YOU WADDLE TOO? 🐧", "#FFEB3B")
        ]
    },
    {
        "id": "scene3_loop",
        "image": "assets/cocomelon_scene3_loop.png",
        "audio": "assets/audio/cocomelon_scene3.mp3",
        "captions": [
            (0.0, 2.8, "✨ 1... 2... 3... GO! ✨", "#00E676"),
            (2.8, 6.3, "🐾 WADDLE WADDLE! 🐾", "#FFD700")
        ]
    }
]

def make_cocomelon_badge(text, text_color):
    """Creates a high-contrast bouncy bubble caption badge."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font = ImageFont.truetype(FONT_PATH, 74)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0] + 120
    th = bbox[3] - bbox[1] + 70
    
    # Place pill in top third
    x0 = (W - tw) // 2
    y0 = 150
    x1 = x0 + tw
    y1 = y0 + th
    
    # Thick shadow + bright white candy pill
    draw.rounded_rectangle([x0 + 8, y0 + 8, x1 + 8, y1 + 8], radius=40, fill=(0, 0, 0, 110))
    draw.rounded_rectangle([x0, y0, x1, y1], radius=40, fill=(255, 255, 255, 250), outline=(255, 204, 0, 255), width=10)
    
    # Text with heavy black stroke
    tx = (W - (bbox[2] - bbox[0])) // 2
    ty = y0 + 20
    
    for dx, dy in [(-3,-3), (3,-3), (-3,3), (3,3), (0,3), (0,-3), (3,0), (-3,0)]:
        draw.text((tx + dx, ty + dy), text, font=font, fill=(0, 0, 0, 255))
    draw.text((tx, ty), text, font=font, fill=text_color)
    
    return np.array(overlay)

def render_scene(cfg):
    raw_img = Image.open(cfg["image"]).convert("RGB")
    img = raw_img.resize((W, H), Image.Resampling.LANCZOS)
    img_np = np.array(img)
    
    audio = AudioFileClip(cfg["audio"])
    dur = audio.duration
    base = ImageClip(img_np, duration=dur)
    
    layers = [base]
    for start_t, end_t, text, color in cfg["captions"]:
        c_dur = min(end_t, dur) - start_t
        if c_dur <= 0:
            continue
        badge_np = make_cocomelon_badge(text, color)
        badge_clip = ImageClip(badge_np, duration=c_dur).with_start(start_t)
        layers.append(badge_clip)
        
    return CompositeVideoClip(layers, size=(W, H)).with_duration(dur).with_audio(audio)

def main():
    os.makedirs("output", exist_ok=True)
    out_path = "output/Pixieland_Cocomelon_Style_Short.mp4"
    
    scene_clips = [render_scene(cfg) for cfg in SCENES]
    final_video = concatenate_videoclips(scene_clips, method="compose")
    
    print(f"Exporting Cocomelon-style Short to {out_path}...")
    final_video.write_videofile(
        out_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast"
    )
    print(f"\n[DONE] High-retention Short exported to: {out_path}")

if __name__ == "__main__":
    main()

