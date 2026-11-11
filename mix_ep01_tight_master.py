"""
Mixes the synchronized Master Soundtrack for Pixieland Episode 01: The Magic Compass
Total video length: ~83.7s
Audio aligns with all 9 animated scenes:
Scene 1: 0.0s  -> Beat 1 at 0.4s
Scene 2: 9.2s  -> Beat 2 at 9.6s
Scene 3: 18.4s -> Beat 3 at 18.8s
Scene 4: 27.6s -> Beat 4 at 28.0s
Scene 5: 36.8s -> Beat 5 at 37.2s
Scene 6: 46.0s -> Beat 6 at 46.4s
Scene 7: 55.2s -> Beat 7 at 56.0s
Scene 8: 64.4s -> Beat 8 at 65.0s
Scene 9: 73.6s -> Beat 9 at 74.0s (ends 82.8s, video ends 83.7s)
"""
import os
import wave
import struct
import numpy as np
from moviepy import AudioFileClip

AUDIO_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\audio"
SFX_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\sfx"
OUT_SOUNDTRACK = os.path.join(AUDIO_DIR, "ep01_master_tight_soundtrack.wav")
SAMPLE_RATE = 44100
TOTAL_DUR = 84.0

BEATS = [
    {"id": "beat1_garden_butterfly_tight", "start": 0.4},
    {"id": "beat2_compass_glow_tight", "start": 9.6},
    {"id": "beat3_portal_open_tight", "start": 18.8},
    {"id": "beat4_calm_breath_tight", "start": 28.0},
    {"id": "beat5_forest_arrival_tight", "start": 37.2},
    {"id": "beat6_bird_words_tight", "start": 46.4},
    {"id": "beat7_golden_leaf_tight", "start": 56.0},
    {"id": "beat8_journal_sketch_tight", "start": 65.0},
    {"id": "beat9_outro_farewell_tight", "start": 74.0},
]

def load_audio(path):
    clip = AudioFileClip(path)
    arr = clip.to_soundarray(fps=SAMPLE_RATE)
    clip.close()
    if arr.ndim > 1:
        arr = arr.mean(axis=1)
    return arr

def main():
    total_samples = int(TOTAL_DUR * SAMPLE_RATE)
    master_mix = np.zeros(total_samples, dtype=np.float32)

    # 1. Background Music (gentle preschool acoustic marimba/pizzicato)
    bgm_path = os.path.join(AUDIO_DIR, "master_preschool_bgm.wav")
    if os.path.exists(bgm_path):
        bgm_data = load_audio(bgm_path)
        bgm_len = min(len(bgm_data), total_samples)
        bgm_copy = bgm_data[:bgm_len].copy()
        # Fade out in the last 2 seconds
        fade_samples = int(2.0 * SAMPLE_RATE)
        if bgm_len > fade_samples:
            bgm_copy[-fade_samples:] *= np.linspace(1.0, 0.0, fade_samples)
        master_mix[:bgm_len] += bgm_copy * 0.14

    # 2. SFX Cues (Nature ambient, magical portal whoosh, compass chimes)
    chime_f = os.path.join(SFX_DIR, "compass_chime.wav")
    whoosh_f = os.path.join(SFX_DIR, "portal_whoosh.wav")
    birds_f = os.path.join(SFX_DIR, "forest_birds.wav")

    sfx_cues = [
        (birds_f, 0.2, 0.30),
        (chime_f, 9.4, 0.45),
        (whoosh_f, 18.5, 0.40),
        (birds_f, 36.8, 0.35),
        (birds_f, 46.0, 0.40),
        (chime_f, 55.5, 0.45),
        (chime_f, 73.5, 0.40),
    ]
    for sf, st, vol in sfx_cues:
        if os.path.exists(sf):
            arr = load_audio(sf)
            s_idx = int(st * SAMPLE_RATE)
            e_idx = min(s_idx + len(arr), total_samples)
            if e_idx > s_idx:
                master_mix[s_idx:e_idx] += arr[:e_idx - s_idx] * vol

    # 3. Voice Beats
    for b in BEATS:
        vf = os.path.join(AUDIO_DIR, f"{b['id']}.mp3")
        if os.path.exists(vf):
            arr = load_audio(vf)
            s_idx = int(b["start"] * SAMPLE_RATE)
            e_idx = min(s_idx + len(arr), total_samples)
            if e_idx > s_idx:
                master_mix[s_idx:e_idx] += arr[:e_idx - s_idx] * 1.05

    # Normalize to -0.8 dB peak
    max_val = np.max(np.abs(master_mix))
    if max_val > 0.90:
        master_mix = (master_mix / max_val) * 0.90

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

    print(f"[SUCCESS] Mixed tight master soundtrack: {OUT_SOUNDTRACK} (dur={TOTAL_DUR}s)")

if __name__ == "__main__":
    main()

