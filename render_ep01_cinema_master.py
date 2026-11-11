"""
Pixieland Episode 01: The Magic Compass (Master 16:9 Landscape Edition)
Full Duration: 178 seconds (~3 minutes)
Format: 1920x1080 Full HD Landscape (16:9)
Style: High-end preschool TV animation, smooth continuous camera motion,
seamless cross-dissolves, zero text on screen, crystal-clear natural child voice.
"""
import os
import sys
import numpy as np
from PIL import Image
from moviepy import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips,
    CompositeVideoClip
)

SCENES_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\scenes"
AUDIO_PATH = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\audio\ep01_master_soundtrack.wav"
OUT_VIDEO = r"C:\Users\Mattia\YouTubeKids\output\Pixieland_Episode01_The_Magic_Compass_16x9_Full.mp4"

TARGET_W = 1920
TARGET_H = 1080
CROSSFADE_DUR = 1.0 # 1.0 second smooth cross-dissolve

# Timeline breakdown (durations for each scene in seconds)
# Sum minus crossfades = ~178 seconds
SCENE_SPECS = [
    {
        "id": "scene1",
        "file": os.path.join(SCENES_DIR, "scene1_garden_butterfly.png"),
        "duration": 18.5,
        "motion": "zoom_in", # gentle push-in
        "zoom_start": 1.0,
        "zoom_end": 1.08
    },
    {
        "id": "scene2",
        "file": os.path.join(SCENES_DIR, "scene2_compass_glow.png"),
        "duration": 16.5,
        "motion": "pan_left",
        "zoom_start": 1.05,
        "zoom_end": 1.12
    },
    {
        "id": "scene3",
        "file": os.path.join(SCENES_DIR, "scene3_portal_breath.png"),
        "duration": 33.5,
        "motion": "zoom_in",
        "zoom_start": 1.0,
        "zoom_end": 1.10
    },
    {
        "id": "scene4",
        "file": os.path.join(SCENES_DIR, "scene4_forest_wonder.png"),
        "duration": 17.5,
        "motion": "zoom_out", # expansive pull-back
        "zoom_start": 1.12,
        "zoom_end": 1.02
    },
    {
        "id": "scene5",
        "file": os.path.join(SCENES_DIR, "scene5_bird_vocabulary.png"),
        "duration": 30.5,
        "motion": "pan_right",
        "zoom_start": 1.03,
        "zoom_end": 1.09
    },
    {
        "id": "scene6",
        "file": os.path.join(SCENES_DIR, "scene6_golden_leaf_symbol.png"),
        "duration": 28.5,
        "motion": "zoom_in",
        "zoom_start": 1.02,
        "zoom_end": 1.11
    },
    {
        "id": "scene7",
        "file": os.path.join(SCENES_DIR, "scene7_explorer_journal.png"),
        "duration": 20.5,
        "motion": "pan_left",
        "zoom_start": 1.04,
        "zoom_end": 1.10
    },
    {
        "id": "scene8",
        "file": os.path.join(SCENES_DIR, "scene8_pixieland_farewell.png"),
        "duration": 19.5,
        "motion": "zoom_out",
        "zoom_start": 1.08,
        "zoom_end": 1.0
    }
]

def make_cinematic_clip(spec):
    img_path = spec["file"]
    if not os.path.exists(img_path):
        raise FileNotFoundError(f"Missing scene image: {img_path}")
        
    pil_img = Image.open(img_path).convert("RGB")
    orig_w, orig_h = pil_img.size
    
    # Scale to fill 1920x1080 with padding for camera motion
    margin = 1.18
    target_canvas_w = int(TARGET_W * margin)
    target_canvas_h = int(TARGET_H * margin)
    
    # Resize preserving aspect ratio
    scale = max(target_canvas_w / orig_w, target_canvas_h / orig_h)
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)
    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # Center crop to target_canvas
    left = (new_w - target_canvas_w) // 2
    top = (new_h - target_canvas_h) // 2
    cropped_img = pil_img.crop((left, top, left + target_canvas_w, top + target_canvas_h))
    
    np_img = np.array(cropped_img)
    duration = spec["duration"]
    motion = spec["motion"]
    z_start = spec["zoom_start"]
    z_end = spec["zoom_end"]
    
    def transform_frame(get_frame, t):
        progress = t / duration
        # Smooth ease-in-out cosine curve
        smooth_p = 0.5 * (1.0 - np.cos(np.pi * progress))
        cur_zoom = z_start + (z_end - z_start) * smooth_p
        
        # Determine crop window inside target_canvas based on motion
        cw = int(TARGET_W / cur_zoom)
        ch = int(TARGET_H / cur_zoom)
        
        # Pan offset
        max_dx = (target_canvas_w - cw)
        max_dy = (target_canvas_h - ch)
        
        if motion == "pan_left":
            cx = int(max_dx * (1.0 - smooth_p))
            cy = int(max_dy * 0.5)
        elif motion == "pan_right":
            cx = int(max_dx * smooth_p)
            cy = int(max_dy * 0.5)
        elif motion == "zoom_in":
            cx = int(max_dx * 0.5)
            cy = int(max_dy * (0.4 + 0.2 * smooth_p))
        else: # zoom_out
            cx = int(max_dx * 0.5)
            cy = int(max_dy * (0.6 - 0.2 * smooth_p))
            
        cx = max(0, min(cx, target_canvas_w - cw))
        cy = max(0, min(cy, target_canvas_h - ch))
        
        frame = np_img[cy:cy+ch, cx:cx+cw]
        frame_pil = Image.fromarray(frame).resize((TARGET_W, TARGET_H), Image.Resampling.BILINEAR)
        return np.array(frame_pil)
        
    base_clip = ImageClip(np_img, duration=duration)
    animated_clip = base_clip.transform(transform_frame)
    return animated_clip

def render_master_episode():
    os.makedirs(os.path.dirname(OUT_VIDEO), exist_ok=True)
    print("=== Building Cinematic Scene Clips ===")
    
    clips = []
    for spec in SCENE_SPECS:
        print(f"Creating animated camera for {spec['id']} (duration={spec['duration']}s)...")
        clip = make_cinematic_clip(spec)
        clips.append(clip)
        
    print(f"\nConcatenating {len(clips)} scenes with {CROSSFADE_DUR}s cross-dissolve transitions...")
    video = concatenate_videoclips(clips, method="compose", padding=-CROSSFADE_DUR)
    
    print(f"Generated Video Duration: {video.duration:.2f}s")
    
    # Attach master soundtrack
    print(f"Attaching Master Soundtrack from {AUDIO_PATH}...")
    audio = AudioFileClip(AUDIO_PATH)
    final_dur = min(video.duration, audio.duration)
    print(f"Synchronizing final video to {final_dur:.2f}s...")
    
    video = video.subclipped(0, final_dur)
    audio = audio.subclipped(0, final_dur)
    final_video = video.with_audio(audio)
    
    print(f"\nExporting Master Broadcast Video (1920x1080 @ 30fps) to: {OUT_VIDEO}...")
    final_video.write_videofile(
        OUT_VIDEO,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast",
        ffmpeg_params=["-pix_fmt", "yuv420p"]
    )
    print(f"\n==========================================")
    print(f"[SUCCESS] Pixieland Episode 01 Complete!")
    print(f"File: {OUT_VIDEO}")
    print(f"Size: {os.path.getsize(OUT_VIDEO) / (1024*1024):.2f} MB")
    print(f"==========================================")

if __name__ == "__main__":
    render_master_episode()

