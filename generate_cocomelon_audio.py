"""
Generate upbeat, rhythmic, syncopated voice lines and sound effects for Short #1.
Optimized for the Cocomelon/Bebefinn loop format (16-18 seconds total).
"""
import asyncio
import edge_tts
import os

VOICE = "en-US-AnaNeural"
RATE = "+10%" # slightly perkier, higher-energy cadence
PITCH = "+3Hz"

short_script = [
    {
        "id": "cocomelon_scene1",
        "text": "Whoa! Brrr! Look, it's a baby penguin!"
    },
    {
        "id": "cocomelon_scene2",
        "text": "He waddles! Waddle, waddle, waddle! Can you waddle like a penguin with me?"
    },
    {
        "id": "cocomelon_scene3",
        "text": "1, 2, 3... GO! Waddle, waddle, waddle!"
    }
]

async def main():
    os.makedirs("assets/audio", exist_ok=True)
    for line in short_script:
        out_path = f"assets/audio/{line['id']}.mp3"
        print(f"Generating audio for {line['id']}...")
        comm = edge_tts.Communicate(line["text"], VOICE, rate=RATE, pitch=PITCH)
        await comm.save(out_path)
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    asyncio.run(main())

