"""
Builds the complete 16:9 Landscape Full HD Master Episode of Pixieland Episode 01: The Magic Compass.
- Full duration: ~178 seconds (~3 minutes)
- Resolution: 1920x1080 Full HD Landscape (16:9)
- Visuals: 8 continuous narrative scenes with bespoke Ken Burns camera motions
- Transitions: Seamless 1.0-second crossfades (xfade=fade) between all scenes
- Zero text overlays / badges on screen
- Audio: Full Master Soundtrack with natural child voice (en-US-AnaNeural),
  SFX (ambient birds, portal whoosh, calming breath, compass chimes), and orchestral marimba/pizzicato BGM.
"""
import os
import subprocess
import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SCENES_DIR = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\scenes"
AUDIO_PATH = r"C:\Users\Mattia\YouTubeKids\ep01_landscape\audio\ep01_master_soundtrack.wav"
OUT_VIDEO = r"C:\Users\Mattia\YouTubeKids\output\Pixieland_Episode01_The_Magic_Compass_16x9_Full.mp4"

# Scene specifications
# dur: raw clip duration including 1.0s overlap for smooth crossfade
SCENES = [
    {
        "id": "scene1",
        "file": os.path.join(SCENES_DIR, "scene1_garden_butterfly.png"),
        "dur": 18.5,
        "zoom_filter": "scale=3840:2160,zoompan=z='min(zoom+0.00025,1.14)':d=555:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
    },
    {
        "id": "scene2",
        "file": os.path.join(SCENES_DIR, "scene2_compass_glow.png"),
        "dur": 16.5,
        "zoom_filter": "scale=3840:2160,zoompan=z='min(zoom+0.00030,1.15)':d=495:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
    },
    {
        "id": "scene3",
        "file": os.path.join(SCENES_DIR, "scene3_portal_breath.png"),
        "dur": 33.5,
        "zoom_filter": "scale=3840:2160,zoompan=z='min(zoom+0.00015,1.12)':d=1005:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
    },
    {
        "id": "scene4",
        "file": os.path.join(SCENES_DIR, "scene4_forest_wonder.png"),
        "dur": 17.5,
        "zoom_filter": "scale=3840:2160,zoompan=z='if(lte(zoom,1.0),1.14,max(1.0,zoom-0.00025))':d=525:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
    },
    {
        "id": "scene5",
        "file": os.path.join(SCENES_DIR, "scene5_bird_vocabulary.png"),
        "dur": 30.5,
        "zoom_filter": "scale=3840:2160,zoompan=z='min(zoom+0.00018,1.14)':d=915:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
    },
    {
        "id": "scene6",
        "file": os.path.join(SCENES_DIR, "scene6_golden_leaf_symbol.png"),
        "dur": 28.5,
        "zoom_filter": "scale=3840:2160,zoompan=z='min(zoom+0.00020,1.14)':d=855:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
    },
    {
        "id": "scene7",
        "file": os.path.join(SCENES_DIR, "scene7_explorer_journal.png"),
        "dur": 20.5,
        "zoom_filter": "scale=3840:2160,zoompan=z='min(zoom+0.00025,1.14)':d=615:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
    },
    {
        "id": "scene8",
        "file": os.path.join(SCENES_DIR, "scene8_pixieland_farewell.png"),
        "dur": 18.0,
        "zoom_filter": "scale=3840:2160,zoompan=z='if(lte(zoom,1.0),1.12,max(1.0,zoom-0.00022))':d=540:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30"
    }
]

def render_scene_clip(scene):
    out_clip = os.path.join(SCENES_DIR, f"{scene['id']}_anim.mp4")
    print(f"Rendering animated scene: {scene['id']} (duration={scene['dur']}s)...")
    cmd = [
        FFMPEG, "-y",
        "-loop", "1",
        "-i", scene["file"],
        "-vf", scene["zoom_filter"],
        "-t", str(scene["dur"]),
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        out_clip
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  -> Generated {out_clip} ({os.path.getsize(out_clip)} bytes)")
        return out_clip
    else:
        print(f"Error rendering {scene['id']}: {res.stderr}")
        return None

def build_master():
    os.makedirs(os.path.dirname(OUT_VIDEO), exist_ok=True)
    clip_paths = []
    for sc in SCENES:
        clip = render_scene_clip(sc)
        if not clip:
            print("Failed to generate one of the clips!")
            return
        clip_paths.append(clip)
        
    print("\n=== Assembling all 8 scenes with smooth crossfades and soundtrack ===")
    
    # Calculate crossfade offsets
    # transition duration = 1.0s
    trans_dur = 1.0
    offsets = []
    cur_time = 0.0
    for idx, sc in enumerate(SCENES[:-1]):
        cur_time += sc["dur"] - trans_dur
        offsets.append(cur_time)
        
    print(f"Crossfade transition offsets: {offsets}")
    
    # Build ffmpeg complex filter for cascading xfades
    # Inputs: -i clip0 -i clip1 ... -i clip7 -i audio
    inputs = []
    for cp in clip_paths:
        inputs.extend(["-i", cp])
    inputs.extend(["-i", AUDIO_PATH])
    
    filter_parts = []
    # [0:v][1:v]xfade=transition=fade:duration=1.0:offset=offsets[0][v01];
    # [v01][2:v]xfade=transition=fade:duration=1.0:offset=offsets[1][v02]; ...
    prev_label = "0:v"
    for idx in range(1, len(clip_paths)):
        next_in = f"{idx}:v"
        out_label = f"v{idx}"
        offset = offsets[idx-1]
        filter_parts.append(
            f"[{prev_label}][{next_in}]xfade=transition=fade:duration={trans_dur}:offset={offset:.2f}[{out_label}]"
        )
        prev_label = out_label
        
    filter_complex = ";".join(filter_parts)
    
    cmd = [
        FFMPEG, "-y",
        *inputs,
        "-filter_complex", filter_complex,
        "-map", f"[{prev_label}]",
        "-map", f"{len(clip_paths)}:a",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUT_VIDEO
    ]
    
    print("\nRunning Master Assembly via FFmpeg...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0 and os.path.exists(OUT_VIDEO):
        size_mb = os.path.getsize(OUT_VIDEO) / (1024 * 1024)
        print("\n===========================================================")
        print(f"🎉 MASTER EPISODE 01 READY: {OUT_VIDEO}")
        print(f"File Size: {size_mb:.2f} MB")
        print("===========================================================")
    else:
        print(f"FFmpeg error: {res.stderr}")

if __name__ == "__main__":
    build_master()

