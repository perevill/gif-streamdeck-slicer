# Stream Deck GIF Slicer

Splits animated GIFs into a grid. G. Colab ready. For a big animated background across all your buttons.

## What it does

- Slices any GIF into X animated pieces that fit the Stream Deck layout
- Handles aspect ratio automatically (crop or resize mode)
- Exports everything as a ZIP file
- Preserves animation speed and looping from the original GIF

## How to use

Just run it in Google Colab:

1. Open a new notebook at [colab.research.google.com](https://colab.research.google.com/)
2. Paste the code
3. Run it and upload your GIF when it asks
4. Download the ZIP file it creates

## Settings

You can tweak these at the top of the script:

```python
cols = 4        # Columns
rows = 2        # Rows
mode = "resize" # "crop" or "resize" - see below
```

**resize mode** (default): Adds black bars to make your GIF fit the 2:1 ratio without cutting anything off.

**crop mode**: Cuts the edges off your GIF to make it exactly 2:1. Might lose some content but no black bars.

## Output files

You'll get a ZIP with 8 files named by position:

```
tile_r1_c1.gif  tile_r1_c2.gif  tile_r1_c3.gif  tile_r1_c4.gif
tile_r2_c1.gif  tile_r2_c2.gif  tile_r2_c3.gif  tile_r2_c4.gif
```

The naming matches the grid layout - r1 is row 1 (top), r2 is row 2 (bottom), c1-c4 are columns left to right.

## Setting up

1. Extract the ZIP
2. Open Stream Deck software
3. Drag each GIF to its matching spot

The files are already named to match the layout, so `tile_r1_c1.gif` goes top-left, `tile_r2_c4.gif` goes bottom-right, etc.

## Tips

- GIFs that are already 2:1 ratio (like 800x400) work best
- If tiles look weird, try switching between resize and crop mode

## License

MIT - do whatever you want with it

---

Made this because I wanted animated backgrounds on my Stream Deck Plus and couldn't find a tool that kept the animations working.
