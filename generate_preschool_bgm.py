"""
Synthesizes a warm, cheerful, gentle music-box / glockenspiel preschool background track.
Key of C Major, 110 BPM, soft harmonic decay, preschool friendly.
"""
import math
import wave
import struct
import numpy as np

SAMPLE_RATE = 44100
TOTAL_DURATION = 22.0 # seconds

def note_freq(semitones_from_c4):
    # C4 = 261.63 Hz
    return 261.63 * (2.0 ** (semitones_from_c4 / 12.0))

# Cheerful pentatonic melody notes (C4, E4, G4, A4, C5, D5, E5, G5)
# Melody in 4-bar cheerful nursery rhyme rhythm
MELODY_NOTES = [
    (0, 0.4), (4, 0.4), (7, 0.4), (12, 0.6), # C - E - G - C5
    (9, 0.4), (7, 0.4), (4, 0.6),             # A - G - E
    (2, 0.4), (4, 0.4), (7, 0.4), (9, 0.6),  # D - E - G - A
    (7, 0.4), (4, 0.4), (0, 0.8),             # G - E - C
    
    (12, 0.4), (14, 0.4), (16, 0.4), (12, 0.6), # C5 - D5 - E5 - C5
    (9, 0.4), (7, 0.4), (12, 0.6),               # A - G - C5
    (7, 0.3), (9, 0.3), (7, 0.3), (4, 0.4),      # G - A - G - E
    (2, 0.4), (4, 0.4), (0, 1.0),                 # D - E - C
]

def synthesize():
    num_samples = int(SAMPLE_RATE * TOTAL_DURATION)
    audio = np.zeros(num_samples, dtype=np.float32)
    
    current_time = 0.0
    while current_time < TOTAL_DURATION:
        for semitone, dur in MELODY_NOTES:
            if current_time >= TOTAL_DURATION:
                break
            freq = note_freq(semitone)
            note_samples = int(SAMPLE_RATE * dur)
            t = np.linspace(0, dur, note_samples, endpoint=False)
            
            # Glockenspiel / marimba waveform: fundamental + soft 2nd & 3rd harmonic
            osc = (
                0.7 * np.sin(2 * np.pi * freq * t) +
                0.2 * np.sin(2 * np.pi * freq * 2 * t) +
                0.1 * np.sin(2 * np.pi * freq * 3 * t)
            )
            # Bell/chime exponential decay envelope
            envelope = np.exp(-4.5 * t / dur)
            note = osc * envelope * 0.18 # gentle volume
            
            start_idx = int(current_time * SAMPLE_RATE)
            end_idx = min(start_idx + note_samples, num_samples)
            audio[start_idx:end_idx] += note[:end_idx - start_idx]
            
            current_time += dur * 0.95 # slight overlap for ringing chimes
            
    out_file = r"C:\Users\Mattia\YouTubeKids\assets\audio\preschool_bgm.wav"
    with wave.open(out_file, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        # convert audio to int16 bytes
        data = bytearray()
        for sample in audio:
            clamped = max(-1.0, min(1.0, sample))
            val = int(clamped * 32767)
            data.extend(struct.pack("<h", val))
        wf.writeframes(data)
    print(f"Generated preschool BGM: {out_file}")

if __name__ == "__main__":
    synthesize()
