import os
import glob
from moviepy import VideoFileClip
from PIL import Image

OUT_DIR = "output/debug/existing_clips_frames"
os.makedirs(OUT_DIR, exist_ok=True)

clips = glob.glob("assets/clips/*.mp4")
print(f"Extracting sample frames from {len(clips)} clips...")
for cp in clips:
    name = os.path.splitext(os.path.basename(cp))[0]
    try:
        v = VideoFileClip(cp)
        mid_time = v.duration / 2.0
        frame = v.get_frame(mid_time)
        out_jpg = os.path.join(OUT_DIR, f"{name}.jpg")
        Image.fromarray(frame).save(out_jpg)
        print(f"  {name}: {v.duration:.2f}s, size={v.size} -> saved {out_jpg}")
        v.close()
    except Exception as e:
        print(f"  Error on {name}: {e}")
