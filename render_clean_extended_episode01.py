"""
Renders the Extended, Cinematic, Text-Free Episode 01: "The Magic Compass"
Duration: ~63 seconds (Full story arc)
Features:
- 100% clean, full-screen 3D Google Vids animation (NO text overlays)
- Studio-grade expressive preschool narrator voice (en-US-AvaNeural)
- Explicit life lessons: Safety first + Kindness to Nature
- Full 5-word curriculum: Hello, Look, Magic, Go, Wow
- Secret Clue: A tiny golden leaf
- Soft acoustic glockenspiel background music at 12% volume
"""
import os
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips
)

W, H = 720, 1280
FPS = 30

SCENES_CONFIG = [
    {
        "id": "beat1_garden_hello",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene1_garden_hello.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_cinema\ep1_beat1_garden_hello.mp3"
    },
    {
        "id": "beat2_garden_question",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene1_garden_hello.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_cinema\ep1_beat2_garden_question.mp3",
        "reverse_first": True # start from looking at gate
    },
    {
        "id": "beat3_compass_magic",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\vids_beat1_compass.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_cinema\ep1_beat3_compass_magic.mp3"
    },
    {
        "id": "beat4_portal_safety",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene3_portal_go.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_cinema\ep1_beat4_portal_safety.mp3"
    },
    {
        "id": "beat5_leaf_nature_lesson",
        "video": r"C:\Users\Mattia\YouTubeKids\assets\clips\ep01_scene4_forest_leaf.mp4",
        "audio": r"C:\Users\Mattia\YouTubeKids\assets\audio\ep01_cinema\ep1_beat5_leaf_nature_lesson.mp3"
    }
]

def make_seamless_clip(video_path, target_duration):
    vclip = VideoFileClip(video_path)
    if vclip.duration >= target_duration:
        return vclip.subclipped(0, target_duration)
    
    # Calculate how many repetitions needed
    reps = int(target_duration / vclip.duration) + 2
    repeated = concatenate_videoclips([vclip] * reps)
    return repeated.subclipped(0, target_duration)

def render_scene(cfg):
    audio = AudioFileClip(cfg["audio"])
    dur = audio.duration
    vclip = make_seamless_clip(cfg["video"], dur)
    return vclip.with_audio(audio)

def main():
    os.makedirs("output", exist_ok=True)
    out_path = r"output\Pixieland_Episode01_The_Magic_Compass_Clean.mp4"
    
    print("--- Assembling Clean Extended Episode 01 ---")
    scene_clips = [render_scene(cfg) for cfg in SCENES_CONFIG]
    full_video = concatenate_videoclips(scene_clips, method="compose")
    total_dur = full_video.duration
    print(f"Total Episode Duration: {total_dur:.2f} seconds")
    
    # Mix soft background glockenspiel
    bgm_path = r"C:\Users\Mattia\YouTubeKids\assets\audio\preschool_bgm.wav"
    if os.path.exists(bgm_path):
        print("Mixing gentle background music at 12% volume...")
        bgm = AudioFileClip(bgm_path)
        from moviepy import concatenate_audioclips
        loops = int(total_dur / bgm.duration) + 1
        bgm_extended = concatenate_audioclips([bgm] * loops).subclipped(0, total_dur)
        bgm_extended = bgm_extended.with_volume_scaled(0.12)
        
        mixed_audio = CompositeAudioClip([full_video.audio, bgm_extended])
        final_video = full_video.with_audio(mixed_audio)
    else:
        final_video = full_video
        
    print(f"Exporting cinematic master to {out_path}...")
    final_video.write_videofile(
        out_path,
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast"
    )
    print(f"\n[DONE] Successfully rendered clean Episode 01: {out_path}")

if __name__ == "__main__":
    main()
