#!/usr/bin/env python3
"""Render the illustrative Outcome Machines introduction video.

Requires Pillow and an ffmpeg executable (pass its path with --ffmpeg).
The visuals contain no customer data or claimed results.
"""

import argparse
import math
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT, FPS = 1280, 720, 24
SCENE_SECONDS = 4
SCENES = 8
INK = "#0a0b0d"
PANEL = "#161a1f"
PANEL_2 = "#1d2228"
PAPER = "#f4f1ea"
DIM = "#a6a7a4"
FAINT = "#6d7276"
ORANGE = "#ff5c28"
LINE = "#3a3b3c"
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_MONO = "/System/Library/Fonts/SFNSMono.ttf"


def font(size, bold=False, mono=False):
    return ImageFont.truetype(FONT_MONO if mono else FONT_BOLD if bold else FONT_REGULAR, size)


def clamp(value, lo=0.0, hi=1.0):
    return max(lo, min(hi, value))


def ease(value):
    value = clamp(value)
    return value * value * (3 - 2 * value)


def txt(draw, xy, text, size, fill=PAPER, bold=False, mono=False, anchor=None):
    draw.text(xy, text, font=font(size, bold, mono), fill=fill, anchor=anchor)


def rounded(draw, box, radius=18, fill=PANEL, outline=None, width=1):
    draw.rounded_rectangle(box, radius, fill=fill, outline=outline, width=width)


def brand_mark(draw, x, y, r=24, phase=0, dark=False):
    background = PAPER if dark else INK
    draw.ellipse((x-r, y-r, x+r, y+r), fill=background)
    # Match the dashed ring and center dot in public/om-symbol-512.svg.
    for i in range(25):
        a0 = i * (360 / 25) + phase
        draw.arc((x-r, y-r, x+r, y+r), a0, a0 + 7.2, fill=ORANGE, width=max(2, int(r / 14.4)))
    inner = r * 0.36
    draw.ellipse((x-inner, y-inner, x+inner, y+inner), fill=ORANGE)


def header(draw, label, index, t):
    brand_mark(draw, 60, 51, 19, t * 8)
    txt(draw, (96, 37), "OUTCOME MACHINES", 20, bold=True)
    txt(draw, (60, 104), label.upper(), 13, ORANGE, mono=True)
    txt(draw, (1218, 39), f"{index:02d} / 06", 13, DIM, mono=True, anchor="ra")
    draw.line((60, 682, 1220, 682), fill=LINE, width=1)
    txt(draw, (60, 690), "ILLUSTRATIVE EXAMPLE  ·  NO CUSTOMER DATA", 11, FAINT, mono=True)
    for dot in range(6):
        draw.ellipse((1120 + dot * 20, 691, 1127 + dot * 20, 698), fill=ORANGE if dot == index - 1 else LINE)


def heading(draw, kicker, lines, body, t):
    reveal = ease(t / 0.55)
    dx = int((1 - reveal) * -24)
    txt(draw, (60 + dx, 173), kicker.upper(), 14, ORANGE, mono=True)
    y = 212
    for line in lines:
        txt(draw, (60 + dx, y), line, 48, bold=True)
        y += 58
    y += 17
    for line in body:
        txt(draw, (60 + dx, y), line, 22, DIM)
        y += 31


def outcome_card(draw, x, y, w, h, label, title, sub="", accent=False):
    rounded(draw, (x, y, x+w, y+h), 16, PANEL_2 if accent else PANEL, ORANGE if accent else LINE, 2 if accent else 1)
    txt(draw, (x+24, y+20), label.upper(), 12, ORANGE if accent else FAINT, mono=True)
    txt(draw, (x+24, y+50), title, 25, PAPER, bold=True)
    if sub:
        txt(draw, (x+24, y+h-41), sub, 16, DIM)


def connector(draw, points, color=ORANGE, width=3):
    draw.line(points, fill=color, width=width, joint="curve")
    x1, y1, x2, y2 = points[-4:]
    angle = math.atan2(y2-y1, x2-x1)
    for sign in (-1, 1):
        a = angle + math.pi + sign * 0.55
        draw.line((x2, y2, x2+13*math.cos(a), y2+13*math.sin(a)), fill=color, width=width)


def scene(index, t):
    image = Image.new("RGB", (WIDTH, HEIGHT), INK)
    draw = ImageDraw.Draw(image)
    if index == 0:
        for i in range(12):
            x = 820 + i * 48
            draw.line((x, 0, x, HEIGHT), fill="#16181a", width=1)
        for i in range(9):
            y = 95 + i * 70
            draw.line((0, y, WIDTH, y), fill="#16181a", width=1)
        brand_mark(draw, 965, 341, 160, t * 23)
        draw.ellipse((726, 102, 1204, 580), outline=LINE, width=1)
        txt(draw, (70, 250), "OUTCOME", 72, bold=True)
        txt(draw, (70, 330), "MACHINES", 72, ORANGE, bold=True)
        txt(draw, (74, 440), "AI systems that work on a", 26, DIM)
        txt(draw, (74, 476), "business outcome.", 26, DIM)
        txt(draw, (74, 644), "MONITOR  →  EXPLAIN  →  RECOMMEND  →  EXECUTE  →  LEARN", 13, FAINT, mono=True)
    elif index == 1:
        header(draw, "Start with a goal", 1, t)
        heading(draw, "One measurable outcome", ["Recover lost", "revenue."], ["Give the system a goal and the", "decisions that can move it."], t)
        rounded(draw, (662, 157, 1218, 602), 22, PANEL, LINE)
        txt(draw, (702, 195), "OUTCOME MACHINE  /  01", 14, ORANGE, mono=True)
        txt(draw, (702, 248), "Revenue Recovery", 34, bold=True)
        draw.line((702, 313, 1178, 313), fill=LINE, width=2)
        txt(draw, (702, 347), "PRIMARY MEASURE", 13, FAINT, mono=True)
        txt(draw, (702, 384), "Recovered revenue", 30, PAPER, bold=True)
        txt(draw, (702, 461), "OPERATING FOCUS", 13, FAINT, mono=True)
        txt(draw, (702, 499), "Stockouts  /  supply gaps  /  allocation", 18, DIM)
        rounded(draw, (702, 554, 894, 582), 12, ORANGE)
        txt(draw, (798, 558), "GOAL SELECTED", 12, INK, bold=True, mono=True, anchor="ma")
    elif index == 2:
        header(draw, "Monitor", 2, t)
        heading(draw, "Detect the signal", ["See the gap", "while it matters."], ["Demand is rising where inventory", "cover is falling."], t)
        rounded(draw, (652, 157, 1218, 602), 22, PANEL, LINE)
        txt(draw, (687, 191), "STORE / SKU SIGNALS", 14, FAINT, mono=True)
        outcome_card(draw, 686, 246, 496, 138, "Alert", "Inventory cover below target", "Fast-moving SKU · high-demand region", True)
        outcome_card(draw, 686, 405, 237, 149, "Context", "Demand rising", "Regional trend")
        outcome_card(draw, 945, 405, 237, 149, "Context", "Supply delayed", "Replenishment")
        pulse = 5 + 6 * (0.5 + 0.5 * math.sin(t * 5))
        draw.ellipse((1140-pulse, 265-pulse, 1140+pulse, 265+pulse), outline=ORANGE, width=3)
    elif index == 3:
        header(draw, "Explain", 3, t)
        heading(draw, "Understand the cause", ["Connect what", "changed."], ["The signal is tied to demand,", "available stock, and supplier timing."], t)
        rounded(draw, (652, 157, 1218, 602), 22, PANEL, LINE)
        nodes = [(756, 280, "Demand"), (1018, 280, "Inventory"), (887, 446, "Supplier")]
        connector(draw, (802, 280, 966, 280), FAINT)
        connector(draw, (1000, 320, 921, 416), FAINT)
        connector(draw, (842, 416, 774, 320), FAINT)
        for x, y, label in nodes:
            draw.ellipse((x-55, y-55, x+55, y+55), fill=PANEL_2, outline=ORANGE if label == "Inventory" else LINE, width=3)
            txt(draw, (x, y), label, 17, PAPER, bold=True, anchor="mm")
        rounded(draw, (693, 521, 1178, 569), 12, PANEL_2)
        txt(draw, (717, 535), "LIKELY DRIVER", 12, ORANGE, mono=True)
        txt(draw, (867, 533), "Stock in the wrong location", 17, PAPER, bold=True)
    elif index == 4:
        header(draw, "Recommend", 4, t)
        heading(draw, "Choose the next action", ["Recommend the", "move that helps."], ["A specific action, with the evidence", "and expected effect beside it."], t)
        rounded(draw, (652, 157, 1218, 602), 22, PANEL, ORANGE, 2)
        txt(draw, (688, 190), "RECOMMENDED DECISION", 14, ORANGE, mono=True)
        txt(draw, (688, 255), "Reallocate inventory", 32, bold=True)
        txt(draw, (688, 304), "from lower-velocity stores", 25, DIM)
        draw.line((688, 366, 1180, 366), fill=LINE, width=1)
        txt(draw, (688, 396), "EVIDENCE", 12, FAINT, mono=True)
        txt(draw, (688, 430), "Demand  ·  store velocity  ·  available stock", 17, PAPER)
        txt(draw, (688, 488), "EXPECTED EFFECT", 12, FAINT, mono=True)
        txt(draw, (688, 521), "Fewer stockouts in the affected region", 17, PAPER)
    elif index == 5:
        header(draw, "Execute", 5, t)
        heading(draw, "Govern the action", ["The owner stays", "in control."], ["Policy routes the recommendation", "for review before execution."], t)
        rounded(draw, (652, 157, 1218, 602), 22, PANEL, LINE)
        outcome_card(draw, 686, 211, 496, 120, "Review", "Merchandising owner", "Evidence and constraints visible", True)
        connector(draw, (936, 346, 936, 393), ORANGE)
        outcome_card(draw, 686, 410, 496, 120, "After approval", "Inventory transfer workflow", "Action recorded for measurement")
        rounded(draw, (933, 555, 1182, 580), 12, ORANGE)
        txt(draw, (1057, 558), "GOVERNED ACTION", 11, INK, bold=True, mono=True, anchor="ma")
    elif index == 6:
        header(draw, "Learn", 6, t)
        heading(draw, "Measure the outcome", ["See what", "actually changed."], ["Compare the observed result with", "the baseline. Use it next cycle."], t)
        rounded(draw, (652, 157, 1218, 602), 22, PANEL, LINE)
        txt(draw, (686, 190), "RECOVERED SALES / MEASUREMENT WINDOW", 13, FAINT, mono=True)
        for i in range(4):
            y = 290 + i * 70
            draw.line((690, y, 1172, y), fill=LINE, width=1)
        baseline = [(702, 505), (780, 490), (858, 469), (936, 453), (1014, 438), (1092, 425), (1168, 409)]
        actual = [(702, 505), (780, 486), (858, 457), (936, 421), (1014, 380), (1092, 348), (1168, 321)]
        draw.line(baseline, fill=FAINT, width=4, joint="curve")
        count = max(2, int(2 + ease(t / 2.7) * (len(actual)-2)))
        draw.line(actual[:count], fill=ORANGE, width=5, joint="curve")
        txt(draw, (695, 549), "— BASELINE", 12, FAINT, mono=True)
        txt(draw, (936, 549), "— OBSERVED", 12, ORANGE, mono=True)
    else:
        for radius in (166, 213, 264):
            draw.ellipse((640-radius, 328-radius, 640+radius, 328+radius), outline=LINE, width=1)
        brand_mark(draw, 640, 274, 111, t * 20)
        txt(draw, (640, 436), "OUTCOME MACHINES", 51, PAPER, bold=True, anchor="ma")
        txt(draw, (640, 508), "Pick a goal. Deploy a machine.", 27, DIM, anchor="ma")
        txt(draw, (640, 645), "OUTCOMEMACHINES.COM", 16, ORANGE, mono=True, anchor="ma")
    return image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ffmpeg", default=shutil.which("ffmpeg"))
    parser.add_argument("--output", default="public/outcome-machines-demo.mp4")
    parser.add_argument("--poster", default="public/outcome-machines-demo-poster.png")
    args = parser.parse_args()
    if not args.ffmpeg:
        parser.error("ffmpeg is required; pass --ffmpeg /path/to/ffmpeg")
    poster = scene(0, 1.5)
    poster.save(args.poster)
    cmd = [args.ffmpeg, "-y", "-f", "rawvideo", "-pixel_format", "rgb24", "-video_size", f"{WIDTH}x{HEIGHT}", "-framerate", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "medium", "-crf", "19", "-movflags", "+faststart", args.output]
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    frames_per_scene = SCENE_SECONDS * FPS
    try:
        for frame in range(SCENES * frames_per_scene):
            index = frame // frames_per_scene
            local = (frame % frames_per_scene) / FPS
            image = scene(index, local)
            if local > SCENE_SECONDS - 0.55 and index < SCENES - 1:
                amount = ease((local - (SCENE_SECONDS - 0.55)) / 0.55)
                image = Image.blend(image, scene(index + 1, 0), amount)
            process.stdin.write(image.tobytes())
        process.stdin.close()
        error = process.stderr.read().decode("utf-8", errors="replace")
        if process.wait() != 0:
            raise RuntimeError(error[-3000:])
    except Exception:
        process.kill()
        raise
    print(f"Rendered {SCENES * SCENE_SECONDS}s video: {args.output}")


if __name__ == "__main__":
    main()
