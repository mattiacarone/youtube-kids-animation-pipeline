import os
import sys
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image
from moviepy import VideoFileClip, AudioFileClip, concatenate_videoclips

load_dotenv()

API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")

VEO_SCENES = [
    {
        "id": "clip1_arrival",
        "image_path": "assets/scene1_penguin.jpg",
        "prompt": (
            "2D modern cartoon animation, fluid motion: Pixi, the cute 5-year-old child in a yellow hoodie, "
            "crouches on the sparkling Antarctic ice. Pixi blinks with big expressive green eyes, smiles brightly, "
            "and holds up the golden compass which spins gently with glowing golden star sparkles. "
            "The chubby baby penguin in front of Pixi flaps its tiny flippers excitedly. "
            "Pastel colors, charming preschool animation, smooth 30fps motion, camera slowly zooms in."
        ),
        "duration": 5, # seconds
        "audio_path": "assets/audio/scene1.mp3"
    },
    {
        "id": "clip2_waddle",
        "image_path": "assets/scene2_waddle.jpg",
        "prompt": (
            "2D cartoon animation: Pixi and the fluffy baby penguin are waddling side by side across the snow. "
            "Pixi has arms stretched out like little penguin wings, swaying side to side in a funny waddling motion, laughing. "
            "The baby penguin waddles synchronously with its little feet pattering on the snow. "
            "In the background, the cute baby seal claps its flippers happily. "
            "Vibrant colors, funny playful preschool cartoon motion, smooth animation."
        ),
        "duration": 5,
        "audio_path": "assets/audio/scene2.mp3"
    },
    {
        "id": "clip3_crystal",
        "image_path": "assets/scene3_crystal.jpg",
        "prompt": (
            "2D cartoon animation: The cute baby penguin hops cheerfully on one foot, proudly holding up a glowing magical "
            "turquoise crystal that pulses with soft magical light. Pixi smiles cheerfully and waves one hand at the viewer, "
            "saying goodbye. The golden compass continues to emit subtle sparkles. "
            "Soft pastel sunset lighting, heartwarming preschool cartoon animation, smooth fluid movement."
        ),
        "duration": 5,
        "audio_path": "assets/audio/scene3.mp3"
    }
]

def generate_veo_clip(client, scene_cfg, out_path):
    print(f"\n[Veo] Requesting video generation for: {scene_cfg['id']}...")
    print(f"Prompt: {scene_cfg['prompt']}")

    # Check if reference image exists (used as the first frame so Pixi stays on-model)
    reference_image = None
    if os.path.exists(scene_cfg["image_path"]):
        print(f"Using reference image: {scene_cfg['image_path']}")
        reference_image = types.Image.from_file(location=scene_cfg["image_path"])

    config_args = {
        "aspect_ratio": "9:16",
        "negative_prompt": "ugly, deformed, photorealistic, scary, jittery, low quality, dark, watermark",
    }

    try:
        if reference_image:
            operation = client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=scene_cfg["prompt"],
                image=reference_image,
                config=types.GenerateVideosConfig(**config_args)
            )
        else:
            operation = client.models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=scene_cfg["prompt"],
                config=types.GenerateVideosConfig(**config_args)
            )

        print("Generation started. Waiting for Google AI Studio Veo to render video frames...")
        while not operation.done:
            time.sleep(15)
            operation = client.operations.get(operation)
            print(".", end="", flush=True)

        print(f"\nCompleted! Downloading {scene_cfg['id']}...")
        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save(out_path)
        print(f"Saved: {out_path}")
        return out_path

    except Exception as e:
        print(f"Error generating clip with Veo: {e}")
        return None

def main():
    if not API_KEY:
        print("\n" + "="*70)
        print("[!] GEMINI_API_KEY not found in environment or .env file.")
        print("To generate full AI video animation with Google Veo in Google AI Studio:")
        print("1. Visit: https://aistudio.google.com/")
        print("2. Click 'Get API key' and copy your key.")
        print("3. Create a '.env' file in this folder with: GEMINI_API_KEY=your_key_here")
        print("="*70 + "\n")
        return

    client = genai.Client(api_key=API_KEY)
    os.makedirs("output/veo_clips", exist_ok=True)

    rendered_clips = []
    for scene in VEO_SCENES:
        out_clip_path = f"output/veo_clips/{scene['id']}.mp4"
        if os.path.exists(out_clip_path):
            print(f"Found existing clip: {out_clip_path}")
            rendered_clips.append(out_clip_path)
            continue

        result = generate_veo_clip(client, scene, out_clip_path)
        if result:
            rendered_clips.append(result)

    if len(rendered_clips) == len(VEO_SCENES):
        from moviepy import vfx
        print("\nAll animated clips rendered! Assembling final Short with Pixi's voiceover...")
        scene_videos = []
        for clip_path, scene in zip(rendered_clips, VEO_SCENES):
            video = VideoFileClip(clip_path)
            voice = AudioFileClip(scene["audio_path"])
            # Loop the animation if the voice line is longer than the Veo clip
            if voice.duration > video.duration:
                video = video.with_effects([vfx.Loop(duration=voice.duration)])
            else:
                video = video.subclipped(0, voice.duration)
            scene_videos.append(video.with_audio(voice))
        final_video = concatenate_videoclips(scene_videos, method="compose")
        final_out = "output/Pixi_Wobbly_Penguin_ANIMATED.mp4"
        final_video.write_videofile(final_out, fps=30, codec="libx264", audio_codec="aac")
        print(f"\n[SUCCESS] Animated YouTube Short created at: {final_out}")

if __name__ == "__main__":
    main()
