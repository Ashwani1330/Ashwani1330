# Deep Blue terminal card

`deep-blue.gif` is a real cool-retro-term recording using its **built-in Deep Blue
profile**, not an imported theme. The 3:2 capture is 1200 × 800 with font scale
0.95; the GIF is 720 × 480, approximately 30 fps, and 7.1 seconds. It uses 32 colors
without dithering and light noise reduction to keep the download small. The cut
is selected to reduce the visible jump in the CRT effect.

The card centers the hoodie beside the profile text, with the name first and a
single `present day. present time.` footer. Python prints the card once;
cool-retro-term supplies the animation. No AI-generated artwork or pip packages.

## Preview

Requires Python 3, ImageMagick (`magick`), and cool-retro-term. Select
**Profiles → Deep Blue**, set the terminal font scale to **0.95**, and size the
window to **1200 × 800**. Run from the repository root:

```sh
python assets/terminal/profile.py --braille --hold
```

The hoodie is the default image. `--image /path/to/image.png` selects another
local image; omit `--braille` for conventional ASCII, or use `--plain` for plain
text. Keep at least **86 columns × 26 rows** available. The recorded preset's
font works with the hoodie; no custom theme or font import is required.

`--hold` uses the alternate screen and hides the cursor; Ctrl+C restores both.
Edit `INFO` in `profile.py` to update the copy. Check the script with:

```sh
python assets/terminal/profile.py --self-test
```

## Artwork

`lain-hoodie-source.jpg` is the downloaded
[hoodie reference](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGObCSl6WDK2zHUR1RSj7GNeYbCS2O9UIbwgoC80_ADY4ES34KzX6jocE&s=10).
`lain-hoodie.png` is its crop, reproduced with:

```sh
magick assets/terminal/lain-hoodie-source.jpg -crop 310x395+155+25 +repage assets/terminal/lain-hoodie.png
```

ImageMagick extracts contours; Python maps them to 34 columns of Braille cells.
Character: Lain Iwakura, *Serial Experiments Lain*. This is third-party artwork;
source attribution does not grant a redistribution license.

## Record and encode

Record only the terminal window at 1200 × 800 and 60 fps, without the mouse or
desktop decorations. OBS's PipeWire capture works on Niri; the current recording
used FFmpeg's `x11grab` with cool-retro-term running through Xwayland
(`QT_QPA_PLATFORM=xcb QSG_RENDER_LOOP=basic QSG_NO_VSYNC=1`). Keep the window
visible and focused during capture; hidden workspaces can throttle animation.
Keep raw recordings outside the repository.

For this 12-second recording, the cut from 1.2 to 8.3 seconds gave a close loop boundary:

```sh
ffmpeg -i recording.mkv -filter_complex \
  '[0:v]trim=start=1.2:end=8.3,setpts=PTS-STARTPTS,fps=30,scale=720:480:flags=lanczos,hqdn3d=2:2:6:6,split[a][b];[a]palettegen=max_colors=32[p];[b][p]paletteuse=dither=none' \
  -an -loop 0 assets/terminal/deep-blue.gif
```

Choose a new cut for a new recording; CRT motion is not guaranteed to repeat at
these exact frames. Check the loop and readability at the README's 700px width.
