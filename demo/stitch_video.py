from moviepy import VideoFileClip, ColorClip, concatenate_videoclips, ImageClip, CompositeVideoClip, TextClip
import os

# Attempt to find a font
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
if not os.path.exists(FONT_PATH):
    FONT_PATH = "DejaVu-Sans-Bold" # Fallback to name if path fails

def stitch():
    scenes = []
    titles = [
        "Architectural Foundations",
        "Multi-Signal Submission",
        "Weighted-Veto Human Defense",
        "Navigating Uncertainty",
        "Appeals and Transparency",
        "Production Safety and Analytics"
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
        bg_card = ColorClip(size=(1280, 820), color=(30, 30, 30), duration=title_duration)

        main_title = TextClip(
            text=titles[i-1],
            font=FONT_PATH,
            font_size=60,
            color='white',
            method='caption',
            size=(int(1280 * 0.85), None)
        ).with_duration(title_duration).with_position('center')

        title_card = CompositeVideoClip([bg_card, main_title])

        if i in overlays_text:
            sub_text = TextClip(
                text=overlays_text[i],
                font=FONT_PATH,
                font_size=40,
                color='yellow',
                method='caption',
                size=(int(1280 * 0.85), None)
            ).with_duration(title_duration).with_position(('center', 500))
            title_card = CompositeVideoClip([title_card, sub_text])

        # Handle demo clip duration
        if clip.duration > demo_duration:
            demo_clip = clip.subclipped(0, demo_duration)
        else:
            last_frame_time = max(0, clip.duration - 0.1)
            last_frame = clip.subclipped(last_frame_time, clip.duration).with_duration(demo_duration - clip.duration)
            demo_clip = concatenate_videoclips([clip, last_frame])

        # Create 100px Black Header
        header = ColorClip(size=(1280, 100), color=(0, 0, 0), duration=demo_duration)

        # Add technical overlay to header if needed
        if i in overlays_text:
            overlay_label = TextClip(
                text=f"STATUS: {overlays_text[i]}",
                font=FONT_PATH,
                font_size=40,
                color='yellow'
            ).with_duration(demo_duration).with_position((100, 25))
            header = CompositeVideoClip([header, overlay_label])

        # Stack Header on top of Demo Clip (Total height 820)
        # Position the demo clip at y=100
        full_demo_scene = CompositeVideoClip([
            ColorClip(size=(1280, 820), color=(0,0,0), duration=demo_duration),
            header.with_position(('center', 'top')),
            demo_clip.with_position((0, 100))
        ], size=(1280, 820))

        scene = concatenate_videoclips([title_card, full_demo_scene])
        scenes.append(scene)

    final_video = concatenate_videoclips(scenes)
    final_video.write_videofile("provenance_guard_demo.mp4", fps=24, codec="libx264")

if __name__ == "__main__":
    stitch()
