"""
Full Master Audio Pipeline for Pixieland Episode 01: The Magic Compass
Duration: ~180s (3 minutes)
Character: Pixy (en-US-AnaNeural - natural American child voice)
Sound Design: Ambient birds, breeze, portal whoosh, breath, compass chimes, pencil sketch, gentle pizzicato & marimba BGM.
"""
import os
import subprocess
import numpy as np
import wave
import struct
from moviepy import AudioFileClip, CompositeAudioClip, concatenate_audioclips

AUDIO_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\audio"
SFX_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\sfx"
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(SFX_DIR, exist_ok=True)

VOICE = "en-US-AnaNeural"

SCRIPT_BEATS = [
    {
        "id": "beat1_garden_butterfly",
        "text": "Good morning, little explorers! Look at our beautiful garden today. Look! A colorful butterfly! Hello, butterfly! Where are you going?",
        "start_time": 2.0
    },
    {
        "id": "beat2_compass_glows",
        "text": "Wait... what is that sound? Something in my backpack is glowing! Whoa! It's my compass! Look at that golden light! It's spinning!",
        "start_time": 22.0
    },
    {
        "id": "beat3_doorway_lesson",
        "text": "Look! Between the trees... golden sparkles! It's a magical doorway! Hmm... I wonder what's on the other side? It feels a little new... and a little scary. It's okay to feel nervous! Let's take a calming deep breath together. Ahh, that feels better. Curiosity can help us take a safe step forward. Let's explore!",
        "start_time": 46.0
    },
    {
        "id": "beat4_forest_wonder",
        "text": "Wow! Look at this place! It's a giant, beautiful forest! The air is so fresh and peaceful. Look at all the tall green trees and the gentle sunlight!",
        "start_time": 76.0
    },
    {
        "id": "beat5_vocabulary_friends",
        "text": "Listen! Do you hear that? Hello, little bird! Can you say hello? Hello! Look at this big tree! Tree! Can you say tree? Tree! And look at this bright green leaf! Leaf! You did it! We made a new friend in the forest. Friend!",
        "start_time": 98.0
    },
    {
        "id": "beat6_golden_leaf_clue",
        "text": "Where is the bird flying? Let's follow the little path! Oh, look down here! Look at this leaf... it's shiny and golden! And look closely... there's a tiny mystery symbol on it! Hmm... that's strange. I wonder what it means? Our compass is glowing with a tiny star light!",
        "start_time": 128.0
    },
    {
        "id": "beat7_journal_entry",
        "text": "Let's keep our golden leaf safe inside our turquoise backpack. Time to open our Explorer Journal! Let's draw the big tree... the little bird... and our secret symbol. Every adventure teaches us something wonderful!",
        "start_time": 154.0
    },
    {
        "id": "beat8_outro_question",
        "text": "What would YOU like to explore next? You can discover so many amazing things in our world! See you on our next adventure! Bye-bye!",
        "start_time": 174.0
    }
]

def generate_voice_clips():
    clips_info = []
    for b in SCRIPT_BEATS:
        out_file = os.path.join(AUDIO_DIR, f"{b['id']}.mp3")
        print(f"Generating voice for {b['id']}...")
        cmd = [
            "edge-tts",
            "--voice", VOICE,
            "--rate=-2%",
            "--text", b["text"],
            "--write-media", out_file
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(out_file):
            a = AudioFileClip(out_file)
            print(f"  -> Generated {b['id']}: duration={a.duration:.2f}s")
            clips_info.append({
                "file": out_file,
                "start": b["start_time"],
                "duration": a.duration
            })
            a.close()
        else:
            print(f"Error on {b['id']}: {res.stderr}")
    return clips_info

def synthesize_compass_chime(filename, duration=3.0):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    audio = np.zeros(num_samples, dtype=np.float32)
    # Bell chime arpeggio: C6, E6, G6, C7, E7
    notes = [1046.5, 1318.5, 1567.98, 2093.0, 2637.0]
    for i, freq in enumerate(notes):
        offset = int(i * 0.15 * sample_rate)
        note_len = num_samples - offset
        if note_len <= 0:
            break
        t = np.linspace(0, note_len / sample_rate, note_len, endpoint=False)
        envelope = np.exp(-3.5 * t)
        sig = (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)) * envelope * 0.25
        audio[offset:offset+note_len] += sig
    write_wav(filename, audio, sample_rate)

def synthesize_portal_whoosh(filename, duration=4.0):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    # Frequency sweep with warm resonance
    freq = 150 + 400 * np.sin(np.pi * t / duration)
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    envelope = np.sin(np.pi * t / duration) ** 2
    # Add gentle pink-noise shimmer
    noise = np.random.uniform(-0.05, 0.05, num_samples)
    sig = (0.35 * np.sin(phase) + noise) * envelope * 0.3
    write_wav(filename, sig, sample_rate)

def synthesize_bird_chirps(filename, duration=3.5):
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    audio = np.zeros(num_samples, dtype=np.float32)
    chirp_times = [0.2, 0.6, 1.2, 1.5, 2.2, 2.5]
    for ct in chirp_times:
        start_idx = int(ct * sample_rate)
        cdur = 0.12
        clen = int(cdur * sample_rate)
        if start_idx + clen > num_samples:
            break
        t = np.linspace(0, cdur, clen, endpoint=False)
        f_start, f_end = 2800, 3600
        freq = np.linspace(f_start, f_end, clen)
        phase = 2 * np.pi * np.cumsum(freq) / sample_rate
        env = np.sin(np.pi * t / cdur) ** 2
        chirp = np.sin(phase) * env * 0.22
        audio[start_idx:start_idx+clen] += chirp
    write_wav(filename, audio, sample_rate)

def synthesize_full_orchestral_bgm(filename, total_dur=190.0):
    sample_rate = 44100
    num_samples = int(sample_rate * total_dur)
    audio = np.zeros(num_samples, dtype=np.float32)
    
    # Warm marimba & pizzicato chord progression: C - Am - F - G
    chords = [
        [261.63, 329.63, 392.00, 523.25], # C major
        [220.00, 261.63, 329.63, 440.00], # A minor
        [174.61, 220.00, 261.63, 349.23], # F major
        [196.00, 246.94, 293.66, 392.00]  # G major
    ]
    chord_dur = 2.4 # seconds per bar
    t_cur = 0.0
    chord_idx = 0
    while t_cur < total_dur:
        chord = chords[chord_idx % len(chords)]
        chord_idx += 1
        # 4 light pizzicato pulses per bar
        for pulse in range(4):
            pulse_time = t_cur + pulse * (chord_dur / 4.0)
            if pulse_time >= total_dur:
                break
            start_s = int(pulse_time * sample_rate)
            pulse_dur = 0.5
            p_len = min(int(pulse_dur * sample_rate), num_samples - start_s)
            if p_len <= 0:
                break
            t_p = np.linspace(0, p_len / sample_rate, p_len, endpoint=False)
            env = np.exp(-6.0 * t_p / pulse_dur)
            
            # Root note + soft harmonics
            root = chord[pulse % len(chord)]
            note_sig = (0.6 * np.sin(2 * np.pi * root * t_p) + 
                        0.3 * np.sin(4 * np.pi * root * t_p) + 
                        0.1 * np.sin(6 * np.pi * root * t_p)) * env * 0.14
            audio[start_s:start_s+p_len] += note_sig
            
        t_cur += chord_dur
        
    write_wav(filename, audio, sample_rate)

def write_wav(filename, audio_data, sample_rate):
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        data = bytearray()
        for sample in audio_data:
            clamped = max(-1.0, min(1.0, sample))
            val = int(clamped * 32767)
            data.extend(struct.pack("<h", val))
        wf.writeframes(data)
    print(f"  -> Generated SFX/BGM: {filename}")

if __name__ == "__main__":
    print("=== Step 1: Synthesizing Pixy Dialogue Beats ===")
    clips = generate_voice_clips()
    
    print("=== Step 2: Synthesizing Sound Effects ===")
    chime_file = os.path.join(SFX_DIR, "compass_chime.wav")
    portal_file = os.path.join(SFX_DIR, "portal_whoosh.wav")
    bird_file = os.path.join(SFX_DIR, "forest_birds.wav")
    bgm_file = os.path.join(AUDIO_DIR, "master_preschool_bgm.wav")
    
    synthesize_compass_chime(chime_file)
    synthesize_portal_whoosh(portal_file)
    synthesize_bird_chirps(bird_file)
    synthesize_full_orchestral_bgm(bgm_file, total_dur=190.0)
    print("\nAudio components successfully generated!")

