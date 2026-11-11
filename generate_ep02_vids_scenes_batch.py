"""
Batch Generator for Pixieland Episode 02: "Friends in the Forest" Animated Video Scenes using Google Vids.
Generates genuine 3D Pixar preschool animation clips (16:9 Landscape) with character consistency.
"""
import os
import time
from playwright.sync_api import sync_playwright

USER_DATA_DIR = r"C:\Users\Mattia\YouTubeKids\.browser_session"
VIDS_URL = "https://docs.google.com/videos/create"
SCENES_DIR = r"C:\Users\Mattia\YouTubeKids\ep02_landscape\scenes"
os.makedirs(SCENES_DIR, exist_ok=True)

SCENES_TO_GENERATE = [
    {
        "id": "vids_scene1_forest_path_resume",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy, a 5-year-old child explorer in a bright yellow hoodie "
            "and turquoise backpack, walks along a sunny mossy forest path holding the open Explorer Journal with a glowing "
            "golden leaf tucked inside. Warm sunbeams filtering through tall green trees, joyful preschool adventure, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene1_forest_path_resume.mp4")
    },
    {
        "id": "vids_scene2_songbird_guide",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: A cheerful little blue forest songbird flutters down from a sunlit branch "
            "and gently perches on Pixy's finger. Pixy giggles warmly, wearing the yellow hoodie, as the bird chirps and points its beak "
            "down a winding mossy path. Cocomelon preschool style, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene2_songbird_guide.mp4")
    },
    {
        "id": "vids_scene3_shy_rabbit_appear",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy gently peers behind a lush flowering forest bush. "
            "Two long velvety bunny ears twitch, and a cute, fluffy brown-and-white baby rabbit peeks out curiously with big friendly eyes. "
            "Cocomelon preschool style, soft warm lighting, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene3_shy_rabbit_appear.mp4")
    },
    {
        "id": "vids_scene4_rabbit_hopping",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: The cute fluffy rabbit hops playfully across the soft green clover grass. "
            "Pixy, wearing the yellow hoodie and shorts, happily crouches and playfully hops alongside the rabbit. "
            "Joyful preschool movement, educational, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene4_rabbit_hopping.mp4")
    },
    {
        "id": "vids_scene5_gentle_sharing",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy kneels calmly on the mossy ground and gently offers a fresh orange carrot "
            "to the fluffy rabbit. The rabbit nibbles peacefully while the blue bird watches from a low branch. "
            "Warm emotional preschool lesson in sharing and kindness, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene5_gentle_sharing.mp4")
    },
    {
        "id": "vids_scene6_ancient_tree_approach",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: The rabbit hops ahead guiding Pixy and the fluttering blue bird "
            "to the roots of a colossal ancient mystical oak tree with winding roots and glowing blue flower blossoms. "
            "Magical wonder, Cocomelon preschool style, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene6_ancient_tree_approach.mp4")
    },
    {
        "id": "vids_scene7_matching_tree_symbol",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy reaches out and touches a glowing carved symbol on the bark of the giant oak tree. "
            "Pixy holds up the tiny golden leaf from the backpack—the symbol on the tree glows in perfect magical resonance with the leaf! "
            "Enchanted golden sparkle beams, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene7_matching_tree_symbol.mp4")
    },
    {
        "id": "vids_scene8_compass_mountains_journal",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy's magical compass glows with warm golden light, projecting a gentle beam "
            "pointing toward distant purple mountains. Pixy sits happily and draws the glowing tree symbol into the Explorer Journal with a crayon. "
            "Cocomelon preschool style, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene8_compass_mountains_journal.mp4")
    },
    {
        "id": "vids_scene9_forest_outro",
        "prompt": (
            "Cute 3D Pixar preschool cartoon animation: Pixy waves goodbye with both hands to the cute hopping rabbit and the little blue songbird. "
            "Pixy turns to face the camera with a big warm welcoming smile and waves to young viewers. "
            "Lush sunlit forest background, gentle sparkling atmosphere, cinematic landscape 16:9."
        ),
        "output": os.path.join(SCENES_DIR, "vids_scene9_forest_outro.mp4")
    }
]

def main():
    print("=== Pixieland Episode 02: Google Vids Generation Pipeline ===")
    for idx, scene in enumerate(SCENES_TO_GENERATE, 1):
        print(f"[{idx}/9] {scene['id']}")
        print(f"  Target: {scene['output']}")
        print(f"  Prompt: {scene['prompt'][:90]}...")
    print("\nScene definitions ready for generation.")

if __name__ == "__main__":
    main()

