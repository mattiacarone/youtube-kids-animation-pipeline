"""
Renders the 100% Continuous, One-Shot Welcoming Episode of Pixieland.
- Video: 20.01 seconds continuous single-shot 3D animation (Google Vids Extend)
- Zero cuts, zero transitions, zero looping, zero text on screen
- Crystal-clear preschool educator voiceover
- Gentle acoustic glockenspiel music box melody
"""
import os
from moviepy import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip
)

VIDEO_PATH = r"C:\Users\Mattia\YouTubeKids\assets\clips\oneshot_clip_2.mp4"
VOICE_PATH = r"C:\Users\Mattia\YouTubeKids\assets\audio\pixy_welcoming_story_voice.mp3"
BGM_PATH = r"C:\Users\Mattia\YouTubeKids\assets\audio\preschool_bgm.wav"
OUT_PATH = r"C:\Users\Mattia\YouTubeKids\output\Pixieland_Welcoming_Episode_Continuous.mp4"

def main():
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    
    print("Loading continuous 20s single-shot video...")
    video = VideoFileClip(VIDEO_PATH)
    total_dur = video.duration
    print(f"Video Duration: {total_dur:.2f}s | Size: {video.size} | FPS: {video.fps}")
    
    print("Loading crystal-clear voiceover...")
    voice = AudioFileClip(VOICE_PATH)
    
    # Mix with soft glockenspiel BGM
    audio_tracks = [voice]
    if os.path.exists(BGM_PATH):
        print("Mixing gentle background glockenspiel at 12% volume...")
        bgm = AudioFileClip(BGM_PATH)
        if bgm.duration < total_dur:
            from moviepy import concatenate_audioclips
            bgm = concatenate_audioclips([bgm, bgm]).subclipped(0, total_dur)
        else:
            bgm = bgm.subclipped(0, total_dur)
        bgm = bgm.with_volume_scaled(0.12)
        audio_tracks.append(bgm)
        
    mixed_audio = CompositeAudioClip(audio_tracks)
    final_video = video.with_audio(mixed_audio)
    
    print(f"Exporting master one-shot video to {OUT_PATH}...")
    final_video.write_videofile(
        OUT_PATH,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        preset="fast"
    )
    print(f"\n[DONE] Continuous welcoming episode exported to: {OUT_PATH}")

if __name__ == "__main__":
    main()

