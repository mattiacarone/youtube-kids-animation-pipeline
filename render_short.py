import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips

W, H = 1080, 1920
FPS = 30
FONT_PATH = r"C:\Windows\Fonts\comicbd.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = r"C:\Windows\Fonts\arialbd.ttf"

scenes_config = [
    {
        "id": "scene1",
        "image": "assets/scene1.png",
        "audio": "assets/audio/scene1.mp3",
        "captions": [
            (0.0, 5.2, "❄️ WHOA! BRRR! ❄️", "Look where the compass sent us!"),
            (5.2, 11.95, "🐧 IT'S A PENGUIN! 🐧", "Hello little friend!"),
        ],
        "zoom_start": 1.0,
        "zoom_end": 1.08
    },
    {
        "id": "scene2",
        "image": "assets/scene2.png",
        "audio": "assets/audio/scene2.mp3",
        "captions": [
            (0.0, 6.8, "🐾 LOOK! HE WADDLES! 🐾", "Waddle, waddle, waddle!"),
            (6.8, 14.02, "🐧 CAN YOU WADDLE TOO? 🐧", "Waddle, waddle, waddle!"),
        ],
        "zoom_start": 1.08,
        "zoom_end": 1.0
    },
    {
        "id": "scene3",
        "image": "assets/scene3.png",
        "audio": "assets/audio/scene3.mp3",
        "captions": [
            (0.0, 5.8, "✨ YAY! GOOD JOB! ✨", "A sparkly Pixie Crystal!"),
            (5.8, 11.09, "🧭 WHERE NEXT? 🧭", "LET'S EXPLORE!"),
        ],
        "zoom_start": 1.0,
        "zoom_end": 1.06
    }
]

def make_caption_frame(title_text, sub_text):
    """Creates a transparent RGBA image with a bright kid-friendly caption badge."""
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    font_large = ImageFont.truetype(FONT_PATH, 68)
    font_small = ImageFont.truetype(FONT_PATH, 50)
    
    # Calculate text bounds
    bbox_title = draw.textbbox((0, 0), title_text, font=font_large)
    bbox_sub = draw.textbbox((0, 0), sub_text, font=font_small)
    
    tw = max(bbox_title[2] - bbox_title[0], bbox_sub[2] - bbox_sub[0]) + 100
    th = (bbox_title[3] - bbox_title[0]) + (bbox_sub[3] - bbox_sub[1]) + 90
    
    # Position badge near the top third (not blocking characters)
    box_x0 = (W - tw) // 2
    box_y0 = 140
    box_x1 = box_x0 + tw
    box_y1 = box_y0 + th
    
    # Draw soft shadow
    draw.rounded_rectangle([box_x0 + 6, box_y0 + 6, box_x1 + 6, box_y1 + 6], radius=32, fill=(0, 0, 0, 90))
    # Draw background pill with yellow/white gradient fill
    draw.rounded_rectangle([box_x0, box_y0, box_x1, box_y1], radius=32, fill=(255, 255, 255, 240), outline=(255, 204, 0, 255), width=8)
    
    # Draw Title text (Vibrant Coral/Blue)
    tx_title = (W - (bbox_title[2] - bbox_title[0])) // 2
    ty_title = box_y0 + 20
    draw.text((tx_title + 3, ty_title + 3), title_text, font=font_large, fill=(100, 100, 100, 150))
    draw.text((tx_title, ty_title), title_text, font=font_large, fill=(0, 140, 200, 255))
    
    # Draw Subtitle text (Dark, readable)
    tx_sub = (W - (bbox_sub[2] - bbox_sub[0])) // 2
    ty_sub = ty_title + (bbox_title[3] - bbox_title[1]) + 20
    draw.text((tx_sub, ty_sub), sub_text, font=font_small, fill=(30, 30, 30, 255))
    
    return np.array(overlay)

def render_scene(cfg):
    print(f"Rendering {cfg['id']}...")
    raw_img = Image.open(cfg["image"]).convert("RGB")
    # Resize raw image to fit 1080x1920
    img = raw_img.resize((W, H), Image.Resampling.LANCZOS)
    img_np = np.array(img)
    
    audio = AudioFileClip(cfg["audio"])
    dur = audio.duration
    
    # Create base ImageClip
    base_clip = ImageClip(img_np, duration=dur)
    
    # Add caption overlays
    layers = [base_clip]
    for start_t, end_t, title_t, sub_t in cfg["captions"]:
        c_dur = min(end_t, dur) - start_t
        if c_dur <= 0:
            continue
        cap_np = make_caption_frame(title_t, sub_t)
        cap_clip = ImageClip(cap_np, duration=c_dur).with_start(start_t)
        layers.append(cap_clip)
        
    scene_video = CompositeVideoClip(layers, size=(W, H)).with_duration(dur).with_audio(audio)
    return scene_video

def main():
    os.makedirs("output", exist_ok=True)
    out_video_path = "output/Pixi_Wobbly_Penguin_Short.mp4"
    
    scene_clips = []
    for cfg in scenes_config:
        clip = render_scene(cfg)
        scene_clips.append(clip)
        
    print("\nConcatenating full Short...")
    final_video = concatenate_videoclips(scene_clips, method="compose")
    
    print(f"Exporting final video to {out_video_path} at {FPS} FPS...")
    final_video.write_videofile(
        out_video_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="medium"
    )
    print(f"\n[DONE] Full Short successfully rendered at: {out_video_path}")

if __name__ == "__main__":
    main()

