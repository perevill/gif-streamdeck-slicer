from PIL import Image, ImageSequence
from google.colab import files
import os
import zipfile

# Upload your GIF
print("Upload your GIF file")
uploaded = files.upload()
gif_path = list(uploaded.keys())[0]
print(f"Got it: {gif_path}")

# Config
cols = 4  # Stream Deck Plus has 4 columns
rows = 2  # and 2 rows
mode = "resize"  # or "crop" - resize adds black bars, crop cuts edges

output_folder = "gif_tiles"
os.makedirs(output_folder, exist_ok=True)

# Load the GIF
gif = Image.open(gif_path)
duration = gif.info.get("duration", 100)
loop = gif.info.get("loop", 0)
w, h = gif.size

target_ratio = cols / rows
current_ratio = w / h

print(f"Original: {w}x{h} (ratio: {current_ratio:.2f})")
print(f"Making {cols}x{rows} grid = {cols*rows} tiles")
print(f"Mode: {mode}")

# Figure out how to fit it to 4:2 ratio
if mode == "crop":
    # Cut off edges to match ratio
    if current_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        crop_box = (left, 0, left + new_w, h)
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        crop_box = (0, top, w, top + new_h)
else:
    # Add bars to match ratio
    if current_ratio > target_ratio:
        new_h = int(w / target_ratio)
        new_w = w
    else:
        new_w = int(h * target_ratio)
        new_h = h
    crop_box = None

# Process each frame
frames = []
for frame in ImageSequence.Iterator(gif):
    frame = frame.convert("RGBA")
    
    if mode == "crop" and crop_box:
        frame = frame.crop(crop_box)
    elif mode == "resize":
        frame = frame.resize((new_w, new_h), Image.LANCZOS)
    
    frames.append(frame)

# Calculate tile size
w, h = frames[0].size
tile_w = w // cols
tile_h = h // rows

print(f"Each tile: {tile_w}x{tile_h}")

# Split each frame into tiles
tiles = {}
for r in range(rows):
    for c in range(cols):
        tiles[(r, c)] = []

for frame in frames:
    for r in range(rows):
        for c in range(cols):
            x = c * tile_w
            y = r * tile_h
            tile = frame.crop((x, y, x + tile_w, y + tile_h))
            tiles[(r, c)].append(tile)

# Save each tile as an animated GIF
saved = []
for (r, c), tile_frames in tiles.items():
    filename = f"tile_r{r+1}_c{c+1}.gif"
    path = os.path.join(output_folder, filename)
    
    tile_frames[0].save(
        path,
        save_all=True,
        append_images=tile_frames[1:],
        duration=duration,
        loop=loop,
        disposal=2,
        optimize=False,
        transparency=0
    )
    
    saved.append(filename)
    print(f"Saved: {filename}")

# Zip everything up
zip_name = "streamdeck_plus_tiles.zip"
with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
    for f in saved:
        z.write(os.path.join(output_folder, f), f)

print(f"\n done! Downloading {zip_name}")
files.download(zip_name)
