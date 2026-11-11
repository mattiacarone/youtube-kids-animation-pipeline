"""
Mixes all dialogue beats, sound effects, ambient cues, and musical score
into one seamless master soundtrack for Pixieland Episode 01.
"""
import os
import wave
import struct
import numpy as np
from moviepy import AudioFileClip

AUDIO_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\audio"
SFX_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\sfx"
OUT_SOUNDTRACK = os.path.join(AUDIO_DIR, "ep01_master_soundtrack.wav")

SAMPLE_RATE = 44100

# Beat placements (in seconds from 0)
BEAT_TIMINGS = [
    ("beat1_garden_butterfly.mp3", 1.5),
    ("beat2_compass_glows.mp3", 18.0),
    ("beat3_doorway_lesson.mp3", 34.0),
    ("beat4_forest_wonder.mp3", 67.0),
    ("beat5_vocabulary_friends.mp3", 84.0),
    ("beat6_golden_leaf_clue.mp3", 114.0),
    ("beat7_journal_entry.mp3", 142.0),
    ("beat8_outro_question.mp3", 162.0),
]

# SFX placements: (filename, start_time, volume_scale)
SFX_TIMINGS = [
    (os.path.join(SFX_DIR, "forest_birds.wav"), 0.5, 0.4),    # garden birds at start
    (os.path.join(SFX_DIR, "compass_chime.wav"), 17.5, 0.6),  # compass chime beat 2
    (os.path.join(SFX_DIR, "portal_whoosh.wav"), 33.0, 0.5),  # portal whoosh beat 3
    (os.path.join(SFX_DIR, "forest_birds.wav"), 66.0, 0.4),   # forest arrival birds
    (os.path.join(SFX_DIR, "forest_birds.wav"), 83.0, 0.5),   # bird meeting beat 5
    (os.path.join(SFX_DIR, "compass_chime.wav"), 126.0, 0.55), # compass star sparkle beat 6
    (os.path.join(SFX_DIR, "compass_chime.wav"), 161.0, 0.5), # compass sparkle outro
]

def load_audio_as_float_array(path, target_sr=SAMPLE_RATE):
    clip = AudioFileClip(path)
    # Convert to mono numpy array
    arr = clip.to_soundarray(fps=target_sr)
    clip.close()
    if arr.ndim > 1:
        arr = arr.mean(axis=1) # mix to mono
    return arr

def main():
    print("Calculating total episode duration...")
    last_beat = BEAT_TIMINGS[-1]
    last_clip = AudioFileClip(os.path.join(AUDIO_DIR, last_beat[0]))
    total_dur = last_beat[1] + last_clip.duration + 4.0 # 4s tail
    last_clip.close()
    
    total_samples = int(total_dur * SAMPLE_RATE)
    master_mix = np.zeros(total_samples, dtype=np.float32)
    print(f"Total soundtrack duration: {total_dur:.2f}s ({total_samples} samples)")
    
    # 1. Add background music
    bgm_path = os.path.join(AUDIO_DIR, "master_preschool_bgm.wav")
    if os.path.exists(bgm_path):
        print("Mixing background orchestral music at 12% level...")
        bgm_data = load_audio_as_float_array(bgm_path)
        bgm_len = min(len(bgm_data), total_samples)
        # Apply gentle 2-second fade-in and 3-second fade-out
        fade_in = int(2.0 * SAMPLE_RATE)
        fade_out = int(3.0 * SAMPLE_RATE)
        bgm_copy = bgm_data[:bgm_len].copy()
        if bgm_len > fade_in:
            bgm_copy[:fade_in] *= np.linspace(0.0, 1.0, fade_in)
        if bgm_len > fade_out:
            bgm_copy[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)
        master_mix[:bgm_len] += bgm_copy * 0.12
        
    # 2. Add SFX
    print("Mixing sound effects...")
    for sfx_path, s_time, vol in SFX_TIMINGS:
        if os.path.exists(sfx_path):
            sfx_data = load_audio_as_float_array(sfx_path)
            s_idx = int(s_time * SAMPLE_RATE)
            e_idx = min(s_idx + len(sfx_data), total_samples)
            part_len = e_idx - s_idx
            if part_len > 0:
                master_mix[s_idx:e_idx] += sfx_data[:part_len] * vol
                
    # 3. Add Pixy Dialogue Beats
    print("Mixing Pixy's dialogue...")
    for beat_name, s_time in BEAT_TIMINGS:
        beat_path = os.path.join(AUDIO_DIR, beat_name)
        if os.path.exists(beat_path):
            v_data = load_audio_as_float_array(beat_path)
            s_idx = int(s_time * SAMPLE_RATE)
            e_idx = min(s_idx + len(v_data), total_samples)
            part_len = e_idx - s_idx
            if part_len > 0:
                # Dialogue at full 100% volume
                master_mix[s_idx:e_idx] += v_data[:part_len] * 1.0
                
    # Normalize to prevent any digital clipping (-1 dB headroom)
    max_val = np.max(np.abs(master_mix))
    if max_val > 0.88:
        print(f"Normalizing audio peaks (peak was {max_val:.2f})...")
        master_mix = (master_mix / max_val) * 0.88
        
    # Write master WAV
    print(f"Writing master soundtrack: {OUT_SOUNDTRACK}...")
    with wave.open(OUT_SOUNDTRACK, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        data = bytearray()
        for sample in master_mix:
            clamped = max(-1.0, min(1.0, sample))
            val = int(clamped * 32767)
            data.extend(struct.pack("<h", val))
        wf.writeframes(data)
        
    print(f"\n[SUCCESS] Master soundtrack created! Duration: {total_dur:.2f}s")

if __name__ == "__main__":
    main()

