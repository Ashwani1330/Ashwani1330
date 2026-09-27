#!/usr/bin/env python3
"""Print the profile card; cool-retro-term supplies the CRT animation.

Run: python assets/terminal/profile.py --hold
Check: python assets/terminal/profile.py --self-test
Requires Python 3 and ImageMagick's `magick` command. No pip packages.
Edit INFO below to update the copy; use --image to try another portrait.
"""

import argparse
from itertools import zip_longest
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


HERE = Path(__file__).resolve().parent
ART_WIDTH = 34
RAMP = " .:-=+*#%@"
PALETTE = ("284b78", "376eae", "559dff", "79baff", "9acfff", "c6e5ff")
INFO = [
    "Ashwani Kumar Moudgil",
    "--------------------------------------------",
    "",
    "OS        : CachyOS Linux",
    "Host      : 127.0.0.1",
    "Kernel    : Systems / Backend / XR / Android",
    "WM        : Niri (Wayland)",
    "Focus     : Making software meet reality",
    "Coffee    : Runtime dependency (critical)",
    "Memory    : Stack Overflow (full)",
    "",
    ">> DEVELOPMENT ARSENAL",
    "Languages : Python / C# / Kotlin",
    "Systems   : Linux / Docker / C++",
    "Backend   : FastAPI / Spring Boot / Node.js",
    "XR        : Unity / AR Foundation / OpenXR",
    "Android   : Kotlin / Jetpack Compose",
    "Robotics  : ROS 2 / OpenCV / Gazebo",
    "",
    ">> PRESENT DAY. PRESENT TIME.",
    "Signal    : Connected to the Wired",
    "",
]


def braille_rows(pixels, width, height):
    dots = ((0, 0, 0), (0, 1, 1), (0, 2, 2), (1, 0, 3),
            (1, 1, 4), (1, 2, 5), (0, 3, 6), (1, 3, 7))
    rows = []
    for y in range(0, height, 4):
        row = ""
        for x in range(0, width, 2):
            mask = sum(1 << bit for dx, dy, bit in dots
                       if y + dy < height and x + dx < width
                       and pixels[(y + dy) * width + x + dx] > 127)
            row += chr(0x2800 + mask) if mask else " "
        rows.append(row)
    return rows


def ascii_art(path, braille=False):
    """Map dark ink to bright characters; compensate for tall terminal cells."""
    if not path.is_file():
        raise ValueError(f"Image not found: {path}")
    if not shutil.which("magick"):
        raise ValueError("ImageMagick is required (the magick command).")
    # PAM carries dimensions and raw pixels, avoiding a separate identify call.
    # Contours preserve eyes and the hairclip without filling the face with dots.
    resize = (["-canny", "0x1+10%+30%", "-morphology", "Dilate", "Disk:1",
               "-resize", f"{ART_WIDTH * 2}x", "-threshold", "25%"]
              if braille else ["-resize", f"{ART_WIDTH}x", "-resize", "100x50%",
                               "-unsharp", "0x0.6+0.8+0"])
    result = subprocess.run(
        ["magick", str(path.resolve()) + "[0]", "-background", "white",
         "-alpha", "remove", "-alpha", "off", "-colorspace", "Gray",
         "-auto-level", "-negate", *resize, "-type", "Grayscale", "-depth", "8", "pam:-"],
        capture_output=True, check=True,
    )
    header, pixels = result.stdout.split(b"ENDHDR\n", 1)
    fields = dict(line.split(maxsplit=1) for line in header.splitlines()[1:])
    width, height = int(fields[b"WIDTH"]), int(fields[b"HEIGHT"])
    if (width != ART_WIDTH * (2 if braille else 1) or fields[b"DEPTH"] != b"1"
            or fields[b"MAXVAL"] != b"255" or len(pixels) != width * height):
        raise ValueError("Unexpected grayscale image data from ImageMagick.")
    if braille:
        return braille_rows(pixels, width, height)
    return [
        "".join(RAMP[p * (len(RAMP) - 1) // 255] for p in pixels[i:i + width])
        for i in range(0, len(pixels), width)
    ]


def ink(text, color, plain=False, background=False):
    if plain:
        return text
    rgb = ";".join(str(int(color[i:i + 2], 16)) for i in (0, 2, 4))
    return f"\033[{48 if background else 38};2;{rgb}m{text}\033[0m"


def render(art, plain=False):
    info = [""] + INFO + [
        "            " + "".join(ink("   ", c, plain, True) for c in PALETTE)
    ]
    art = [""] * max(0, (len(info) - len(art)) // 2) + art
    lines = ["", "  " + "layer:01 / identity".ljust(ART_WIDTH + 4) + "protocol: wired", ""]
    for index, (left, right) in enumerate(zip_longest(art, info, fillvalue="")):
        color = "c6e5ff" if index == 1 or right.startswith(">>") else "9acfff"
        lines.append("  " + ink(left.ljust(ART_WIDTH), "79baff", plain)
                     + "    " + ink(right, color, plain))
    lines += ["", "  " + ink("ashwani@wired:~$ ", "559dff", plain)
              + ink("stay connected.", "c6e5ff", plain), ""]
    return "\n".join(lines)


def center_card(card, columns, rows):
    lines = card.splitlines()
    width = max(len(re.sub(r"\x1b\[[0-9;]*m", "", line)) for line in lines)
    left = " " * max(0, (columns - width) // 2)
    top = "\n" * max(0, (rows - len(lines)) // 2)
    return top + "\n".join(left + line for line in lines)


def self_test():
    art = ascii_art(HERE / "lain-portrait.png")
    assert art and all(len(line) == ART_WIDTH for line in art)
    assert all(c in RAMP for line in art for c in line)
    assert len(set("".join(art))) > 5, "Portrait lost its tonal detail"
    plain = render(art, plain=True)
    assert re.sub(r"\x1b\[[0-9;]*m", "", render(art)) == plain
    assert "\x1b" not in plain
    assert center_card("ab\nc", 8, 6) == "\n\n   ab\n   c"
    assert re.sub(r"\x1b\[[0-9;]*m", "", center_card(ink("ab", "9acfff"), 8, 3)) == "\n   ab"
    assert max(map(len, plain.splitlines())) <= 84, "Card will wrap"
    assert "Host      : 127.0.0.1" in plain and "The Wired /" not in plain
    assert len(art) <= 22, "Default portrait should stay compact"
    assert "Python / C# / Kotlin" in plain
    assert all(domain in plain for domain in ("Systems", "Backend", "XR", "Android", "Robotics"))
    assert "ashwani@wired" in render(art * 2, plain=True)
    assert braille_rows(bytes([255] * 8), 2, 4) == ["\u28ff"]
    assert braille_rows(bytes([0] * 8), 2, 4) == [" "]
    assert braille_rows(bytes([255, 0]), 2, 1) == ["\u2801"]
    assert braille_rows(bytes([0] * 7 + [255]), 2, 4) == ["\u2880"]
    dense = ascii_art(HERE / "lain-portrait.png", braille=True)
    assert all(len(line) == ART_WIDTH for line in dense)
    assert all(c == " " or 0x2800 <= ord(c) <= 0x28ff for line in dense for c in line)
    assert len(set("".join(dense))) > 10, "Braille portrait lost its contour detail"
    hoodie = ascii_art(HERE / "lain-hoodie.png")
    assert all(len(line) == ART_WIDTH for line in hoodie)
    try:
        ascii_art(HERE / "missing-image-for-self-test.png")
    except ValueError:
        pass
    else:
        raise AssertionError("Missing images must fail clearly")
    print(f"OK: ASCII/Braille conversion, colors, copy, layout, and missing-image handling "
          f"({max(map(len, plain.splitlines()))} columns x {len(plain.splitlines())} rows).")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=Path, default=HERE / "lain-portrait.png")
    parser.add_argument("--plain", action="store_true", help="omit ANSI colors")
    parser.add_argument("--braille", action="store_true", help="draw detailed contours with Unicode dots")
    parser.add_argument("--hold", action="store_true", help="hold the card for recording; Ctrl+C exits")
    parser.add_argument("--self-test", action="store_true", help="run the small regression check")
    args = parser.parse_args()
    try:
        if args.self_test:
            self_test()
            return
        card = render(ascii_art(args.image, args.braille), args.plain or not sys.stdout.isatty())
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"profile: {error}\n")
    if args.hold and not sys.stdout.isatty():
        parser.error("--hold needs an interactive terminal")
    if not args.hold:
        print(card)
        return
    width = max(map(len, re.sub(r"\x1b\[[0-9;]*m", "", card).splitlines())) + 2
    height = len(card.splitlines()) + 1
    columns, rows = shutil.get_terminal_size()
    if columns < width or rows < height:
        parser.exit(1, f"profile: resize the terminal to at least {width} columns x {height} rows "
                    f"(currently {columns} x {rows}).\n")
    card = center_card(card, columns, rows)
    try:
        print("\033[?1049h\033[2J\033[H\033[?25l" + card, end="", flush=True)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("\033[0m\033[?25h\033[?1049l", end="", flush=True)


if __name__ == "__main__":
    main()
