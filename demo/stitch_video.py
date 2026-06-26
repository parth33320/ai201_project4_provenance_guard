from moviepy import VideoFileClip, ColorClip, concatenate_videoclips, ImageClip, CompositeVideoClip
import os
from PIL import Image, ImageDraw, ImageFont

# Attempt to find a font
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = None

def create_text_image(text, subtext=None, size=(1280, 720), bg=(30, 30, 30), fg=(255, 255, 255), subfg=(200, 200, 0)):
    img = Image.new('RGB', size, color=bg)
    draw = ImageDraw.Draw(img)

    try:
        if FONT_PATH:
            font = ImageFont.truetype(FONT_PATH, 60)
            subfont = ImageFont.truetype(FONT_PATH, 40)
        else:
            font = ImageFont.load_default()
            subfont = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
        subfont = ImageFont.load_default()

    # Draw main text
    draw.text((100, 300), text, fill=fg, font=font)

    # Draw subtext
    if subtext:
        draw.text((100, 400), subtext, fill=subfg, font=subfont)

    return img

def stitch():
    scenes = []
    titles = [
        "Scene 1: Architecture & Context",
        "Scene 2: Multi-Signal Submission",
        "Scene 3: Weighted-Veto Human Defense",
        "Scene 4: Labels & Uncertainty",
        "Scene 5: Appeals Workflow",
        "Scene 6: Rate Limiting & Dashboard"
    ]

    overlays_text = {
        3: "Human Defense Veto Triggered",
        4: "Attribution Neutral Label",
        6: "429 Rate Limit Hit"
    }

    for i in range(1, 7):
        clip_path = f"demo/clips/scene{i}.webm"
        if not os.path.exists(clip_path):
            print(f"Missing {clip_path}")
            continue

        clip = VideoFileClip(clip_path)

        title_duration = 2.0
        demo_duration = 28.0

        # Create title card
        title_img = create_text_image(titles[i-1], subtext=overlays_text.get(i))
        title_img_path = f"demo/clips/title_v2_{i}.png"
        title_img.save(title_img_path)
        title_card = ImageClip(title_img_path, duration=title_duration)

        # Handle demo clip duration
        if clip.duration > demo_duration:
            demo_clip = clip.subclipped(0, demo_duration)
        else:
            last_frame_time = max(0, clip.duration - 0.1)
            last_frame = clip.subclipped(last_frame_time, clip.duration).with_duration(demo_duration - clip.duration)
            demo_clip = concatenate_videoclips([clip, last_frame])

        # Add technical overlay on the demo clip itself if needed
        if i in overlays_text:
            overlay_img = Image.new('RGBA', (1280, 720), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay_img)
            try:
                if FONT_PATH:
                    font = ImageFont.truetype(FONT_PATH, 40)
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()

            # Draw semi-transparent background box for overlay
            text = overlays_text[i]
            # draw.rectangle([80, 50, 600, 110], fill=(0, 0, 0, 160))
            draw.text((100, 60), f"STATUS: {text}", fill=(255, 255, 0, 255), font=font)

            overlay_path = f"demo/clips/overlay_{i}.png"
            overlay_img.save(overlay_path)
            overlay_clip = ImageClip(overlay_path, duration=demo_duration).with_position(("left", "top"))

            demo_clip = CompositeVideoClip([demo_clip, overlay_clip])

        scene = concatenate_videoclips([title_card, demo_clip])
        scenes.append(scene)

    final_video = concatenate_videoclips(scenes)
    final_video.write_videofile("provenance_guard_demo.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    stitch()
