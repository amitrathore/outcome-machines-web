#!/usr/bin/env python3
"""Create a full-length Outcome Machines cut from the Datacentriq demo.

Requires Pillow, ffmpeg, and the original MP4 passed with --source.
"""

import argparse
import importlib.util
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 1920, 1080
INK = "#0a0b0d"
ORANGE = "#ff5c28"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
MONO = "/System/Library/Fonts/SFNSMono.ttf"


def text(draw, xy, value, size, fill=INK, mono=False):
    draw.text(xy, value, font=ImageFont.truetype(MONO if mono else FONT, size), fill=fill)


def mark(draw, x, y, radius, background):
    draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=background)
    for i in range(25):
        start = i * 360 / 25
        draw.arc((x-radius, y-radius, x+radius, y+radius), start, start+7.2, fill=ORANGE, width=max(2, round(radius / 14.4)))
    center = radius * 0.36
    draw.ellipse((x-center, y-center, x+center, y+center), fill=ORANGE)


def transparent():
    return Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))


def make_overlays(directory):
    # Import the existing branded keyframes for consistent intro and end card.
    renderer_path = Path(__file__).with_name("render-outcome-video.py")
    spec = importlib.util.spec_from_file_location("outcome_renderer", renderer_path)
    renderer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(renderer)
    overlays = {}
    overlays["intro"] = renderer.scene(0, 1.5).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
    overlays["outro"] = renderer.scene(7, 1.5).resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)

    side = transparent()
    d = ImageDraw.Draw(side)
    d.rectangle((0, 0, 340, 78), fill="#f8f8f6")
    mark(d, 48, 42, 19, "#f8f8f6")
    text(d, (83, 26), "Outcome Machines", 23)
    overlays["sidebar"] = side

    header = transparent()
    d = ImageDraw.Draw(header)
    d.rectangle((0, 0, 224, 86), fill="#ffffff")
    mark(d, 44, 44, 21, "#ffffff")
    text(d, (82, 20), "Outcome", 22)
    text(d, (82, 44), "Machines", 22)
    overlays["header"] = header

    ask = transparent()
    d = ImageDraw.Draw(ask)
    d.rectangle((1634, 0, 1838, 88), fill="#ffffff")
    d.rounded_rectangle((1650, 23, 1830, 68), radius=9, fill=INK)
    text(d, (1663, 34), "Ask Outcome", 18, "#ffffff")
    overlays["ask"] = ask

    badge = transparent()
    d = ImageDraw.Draw(badge)
    d.rounded_rectangle((26, 992, 600, 1054), radius=12, fill="#0a0b0d", outline="#42372f", width=2)
    mark(d, 62, 1023, 18, INK)
    text(d, (93, 1005), "OUTCOME MACHINES", 19, "#f4f1ea")
    text(d, (316, 1011), "ILLUSTRATIVE DEMO DATA", 15, ORANGE, mono=True)
    overlays["badge"] = badge

    for name, image in overlays.items():
        path = directory / f"{name}.png"
        image.save(path)
        overlays[name] = path
    return overlays


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--ffmpeg", default=shutil.which("ffmpeg"))
    parser.add_argument("--output", default="public/outcome-machines-demo-full.mp4")
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error("ffmpeg is required; pass --ffmpeg /path/to/ffmpeg")
    if not Path(args.source).is_file():
        parser.error("source MP4 does not exist")

    with tempfile.TemporaryDirectory(prefix="outcome-video-") as tmp:
        overlays = make_overlays(Path(tmp))
        order = ["intro", "sidebar", "header", "ask", "badge", "outro"]
        filter_steps = ["[0:v]hue=h=-130:s=1.5[base]"]
        windows = [(0, 6), (6, 17.5), (17.5, 36.5), (17.5, 36.5), (6, 91), (91, 94.5)]
        previous = "base"
        for i, (name, (start, end)) in enumerate(zip(order, windows), start=1):
            output = f"v{i}"
            filter_steps.append(f"[{previous}][{i}:v]overlay=0:0:enable='between(t,{start},{end})':eof_action=repeat[{output}]")
            previous = output
        filter_steps.append(f"[{previous}]format=yuv420p[out]")
        command = [args.ffmpeg, "-y", "-i", args.source]
        for name in order:
            command += ["-i", str(overlays[name])]
        command += ["-filter_complex", ";".join(filter_steps), "-map", "[out]", "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-movflags", "+faststart", "-t", "94.5", args.output]
        process = subprocess.run(command, capture_output=True, text=True)
        if process.returncode:
            raise RuntimeError(process.stderr[-4000:])
    print(f"Rendered full-length Outcome Machines video: {args.output}")


if __name__ == "__main__":
    main()
