# Wired terminal card

The README's `deep-blue.gif` is a real cool-retro-term recording using the built-in
**Deep Blue** profile and the hoodie outline. It is 600 × 470 at 10 fps, matching
the old GIF's dimensions, frame rate, and **60:47** aspect ratio. The capture window
was 1200 × 940 at 20 fps; the exported loop is 6.7 seconds, with its cut chosen to
align the CRT effect closely. The export uses a 64-color palette without dithering.
The terminal font scale is 1.0 (25% larger than the first recording's 0.8), and
`--hold` centers the card horizontally and vertically in the available terminal.

```sh
python assets/terminal/profile.py --image assets/terminal/lain-hoodie.png --braille --hold
```

Use **Profiles → Deep Blue** to reproduce this recording's appearance. The custom
`wired-blue.json` below is an earlier alternative, not the recorded preset.

Existing Lain artwork converted to ASCII by ImageMagick and Python. No generated
artwork, Python packages, or network access needed at runtime.

The default `lain-portrait.png` is a face-and-shoulders crop of your
[fourth reference](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRfYrxjwWuJRhDFTJKR7vXUFlLOFlQMlRwAXyMyylqcN91TKLnjU02356E&s=10).
`lain-hoodie.png` is a tighter crop of your
[hoodie reference](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGObCSl6WDK2zHUR1RSj7GNeYbCS2O9UIbwgoC80_ADY4ES34KzX6jocE&s=10).
Their original downloads are kept as `lain-portrait-source.jpg` and
`lain-hoodie-source.jpg`. No AI-generated artwork is used.

The earlier `lain.png` is retained from [this PNGKey page](https://www.pngkey.com/maxpic/u2e6i1o0a9y3e6q8/)
([image URL](https://www.pngkey.com/png/full/482-4821567_cant-believe-your-shit-lain-iwakura.png)).
Character: Lain Iwakura, *Serial Experiments Lain*. The artwork is third-party
material; source attribution does not grant a redistribution license.

From the repository root:

```sh
python assets/terminal/profile.py
python assets/terminal/profile.py --braille
python assets/terminal/profile.py --image assets/terminal/lain-hoodie.png --braille
python assets/terminal/profile.py --self-test
# Try another local portrait, including the original samurai:
python assets/terminal/profile.py --image /path/to/image.png
```

Edit `INFO` in `profile.py` to update the text. The portrait uses a fixed 34-column
width, vertically centered beside the copy; its height follows the image aspect
ratio, corrected for tall terminal cells. The default portrait is 21 rows tall.
ASCII uses a short density ramp and mild sharpening to separate the facial features.
`--plain` emits plain text. Color is also disabled automatically when redirected.
`--braille` uses edge detection and eight dots per character for a detailed outline
at the same size, without the earlier shaded-dot noise. In cool-retro-term's
Terminal settings, select a system font with Braille glyphs, such as **MesloLGM
Nerd Font**, for that variant. ASCII remains the default and works with the
preset's bundled Departure Mono.

To reproduce the crops from the downloaded originals:

```sh
magick assets/terminal/lain-portrait-source.jpg -crop 300x360+65+5 +repage assets/terminal/lain-portrait.png
magick assets/terminal/lain-hoodie-source.jpg -crop 310x395+155+25 +repage assets/terminal/lain-hoodie.png
```

## Preview in cool-retro-term

In Settings → General → Profile → Import, choose `wired-blue.json`, then load
**Wired Blue**. This preset targets cool-retro-term 2.x (profile format version 2).
Enlarge the window to at least **86 columns × 31 rows**, then run inside it:

```sh
cd /home/ashwani/dev/mics/Ashwani1330
python assets/terminal/profile.py --hold
```

Or, once the preset is imported:

```sh
cool-retro-term --profile 'Wired Blue' --workdir /home/ashwani/dev/mics/Ashwani1330 -e python assets/terminal/profile.py --hold
```

`--hold` uses the alternate screen and hides the cursor. Ctrl+C restores both.
The text stays still; cool-retro-term supplies all CRT animation. Check the
window size first: a terminal opened with `-e` may close when the command exits.

## Record and encode

Use OBS's **Screen Capture (PipeWire)** to capture just the terminal window on
Niri. Hide the mouse pointer, keep the window size fixed, and record a few seconds
after the terminal has settled. Save the recording outside the repository.

For a first 8-second, 20-fps GIF (replace `recording.mkv` with the capture path):

```sh
ffmpeg -ss 2 -t 8 -i recording.mkv -filter_complex \
  '[0:v]fps=20,scale=840:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=128[p];[b][p]paletteuse=dither=bayer:bayer_scale=3' \
  -an -loop 0 assets/terminal/wired-blue.gif
```

Crop any desktop/window decorations before encoding. Inspect legibility at the
README's 700px display width, file size, and the transition from last frame to
first. Adjust the cut to match the glowing scanline's position; arbitrary capture
lengths are not guaranteed seamless. Reduce noise or duration if the GIF is large.

The root README currently displays `./assets/terminal/deep-blue.gif` at 700px wide.
