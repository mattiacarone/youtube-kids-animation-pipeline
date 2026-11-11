import asyncio
import edge_tts
import os

VOICE = "en-US-AnaNeural"
RATE = "+0%"
PITCH = "+2Hz"

lines = [
    {
        "id": "scene1",
        "text": "Whoa! Brrr! Look where my magical compass sent us! Look at that... It's a penguin! Hello little friend!"
    },
    {
        "id": "scene2",
        "text": "Wait, why are you walking like that? Look, he waddles! Waddle, waddle, waddle! Can you waddle like a penguin with me? Waddle, waddle!"
    },
    {
        "id": "scene3",
        "text": "Yay! Good job! Look, he gave us a sparkly crystal! Where should we explore next? Let's explore!"
    }
]

async def main():
    os.makedirs('assets/audio', exist_ok=True)
    for item in lines:
        out_path = f"assets/audio/{item['id']}.mp3"
        print(f"Generating audio for {item['id']}...")
        communicate = edge_tts.Communicate(item['text'], VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(out_path)
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    asyncio.run(main())

