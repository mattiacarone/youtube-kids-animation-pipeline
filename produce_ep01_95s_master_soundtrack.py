"""
Produces the 95-second Master Soundtrack for Pixieland Episode 01 Animated Version.
Duration: 95.0s (Target: 90-100 seconds)
Voice: en-US-AnaNeural (authentic, warm American child voice)
"""
import os
import subprocess
import wave
import struct
import numpy as np
from moviepy import AudioFileClip

AUDIO_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\audio"
SFX_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\sfx"
OUT_SOUNDTRACK = os.path.join(AUDIO_DIR, "ep01_95s_master_soundtrack.wav")
SAMPLE_RATE = 44100
TOTAL_DUR = 95.0

VOICE = "en-US-AnaNeural"

BEATS_95S = [
    {
        "id": "beat1_garden_butterfly_95s",
        "text": "Good morning, little explorers! Look at our beautiful garden today. Look! A colorful butterfly! Hello, butterfly!",
        "start": 1.0
    },
    {
        "id": "beat2_compass_glow_95s",
        "text": "Wait... what's that sound? Something in my backpack is glowing! Whoa! It's my compass! Look at that golden light! It's spinning!",
        "start": 11.0
    },
    {
        "id": "beat3_portal_open_95s",
        "text": "Look between the trees! Golden sparkles! A magical doorway is opening! Wow!",
        "start": 21.0
    },
    {
        "id": "beat4_calm_breath_95s",
        "text": "It feels a little scary. It's okay to feel nervous! Let's take a deep breath together. Ahh! Curiosity helps us take a safe step forward. Let's go!",
        "start": 31.0
    },
    {
        "id": "beat5_forest_arrival_95s",
        "text": "Wow! Look at this place! It's a giant, beautiful forest! Look at all the tall green trees and the gentle sunlight!",
        "start": 43.0
    },
    {
        "id": "beat6_bird_words_95s",
        "text": "Listen! A little bird! Hello, bird! Can you say hello? Hello! Look at this tree! Tree! And look at this leaf! Leaf! We made a new friend. Friend!",
        "start": 53.0
    },
    {
        "id": "beat7_golden_leaf_95s",
        "text": "Look down here! A shiny golden leaf with a mysterious symbol! And our compass is glowing with a tiny star!",
        "start": 65.0
    },
    {
        "id": "beat8_journal_sketch_95s",
        "text": "Time to open our Explorer Journal! Let's draw the big tree... the little bird... and our secret symbol. Every adventure teaches us something new!",
        "start": 75.0
    },
    {
        "id": "beat9_outro_farewell_95s",
        "text": "What would YOU like to explore next? You can discover so many amazing things! See you on our next adventure! Bye-bye!",
        "start": 85.0
    }
]

def load_audio_as_float_array(path, target_sr=SAMPLE_RATE):
    clip = AudioFileClip(path)
    arr = clip.to_soundarray(fps=target_sr)
    clip.close()
    if arr.ndim > 1:
        arr = arr.mean(axis=1)
    return arr

def main():
    print("=== Step 1: Synthesizing 95s Speech Beats ===")
    for b in BEATS_95S:
        out_f = os.path.join(AUDIO_DIR, f"{b['id']}.mp3")
        cmd = [
            "edge-tts",
            "--voice", VOICE,
            "--rate=-2%",
            "--text", b["text"],
            "--write-media", out_f
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            a = AudioFileClip(out_f)
            print(f"  {b['id']}: dur={a.duration:.2f}s (starts at {b['start']}s)")
            a.close()
            
    print("\n=== Step 2: Mixing 95s Master Soundtrack ===")
    total_samples = int(TOTAL_DUR * SAMPLE_RATE)
    master_mix = np.zeros(total_samples, dtype=np.float32)
    
    # 1. Background Music
    bgm_path = os.path.join(AUDIO_DIR, "master_preschool_bgm.wav")
    if os.path.exists(bgm_path):
        bgm_data = load_audio_as_float_array(bgm_path)
        bgm_len = min(len(bgm_data), total_samples)
        bgm_copy = bgm_data[:bgm_len].copy()
        fade_out = int(2.5 * SAMPLE_RATE)
        if bgm_len > fade_out:
            bgm_copy[-fade_out:] *= np.linspace(1.0, 0.0, fade_out)
        master_mix[:bgm_len] += bgm_copy * 0.12
        
    # 2. SFX Cues
    chime_f = os.path.join(SFX_DIR, "compass_chime.wav")
    whoosh_f = os.path.join(SFX_DIR, "portal_whoosh.wav")
    birds_f = os.path.join(SFX_DIR, "forest_birds.wav")
    
    sfx_cues = [
        (birds_f, 0.5, 0.35),
        (chime_f, 10.5, 0.5),
        (whoosh_f, 20.5, 0.45),
        (birds_f, 42.5, 0.35),
        (birds_f, 52.5, 0.45),
        (chime_f, 66.5, 0.5),
        (chime_f, 84.5, 0.45),
    ]
    for sf, st, vol in sfx_cues:
        if os.path.exists(sf):
            arr = load_audio_as_float_array(sf)
            s_idx = int(st * SAMPLE_RATE)
            e_idx = min(s_idx + len(arr), total_samples)
            if e_idx > s_idx:
                master_mix[s_idx:e_idx] += arr[:e_idx - s_idx] * vol
                
    # 3. Dialogue
    for b in BEATS_95S:
        vf = os.path.join(AUDIO_DIR, f"{b['id']}.mp3")
        if os.path.exists(vf):
            arr = load_audio_as_float_array(vf)
            s_idx = int(b["start"] * SAMPLE_RATE)
            e_idx = min(s_idx + len(arr), total_samples)
            if e_idx > s_idx:
                master_mix[s_idx:e_idx] += arr[:e_idx - s_idx] * 1.0
                
    # Normalize peaks (-1 dB)
    max_val = np.max(np.abs(master_mix))
    if max_val > 0.88:
        master_mix = (master_mix / max_val) * 0.88
        
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
        
    print(f"\n[SUCCESS] Generated 95s Master Soundtrack: {OUT_SOUNDTRACK}")

if __name__ == "__main__":
    main()
