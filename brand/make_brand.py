"""Draw the MLPlay developer page graphics for Google Play.

Usage (from the repo root):
    uv run --with pillow python brand/make_brand.py

Writes brand/developer_icon.png (512x512, 32-bit PNG) and
brand/developer_header.jpg (4096x2304, under 1 MB). The art is for the studio,
not one game: a blue "ML" tile, and a header of scattered rounded tiles in
several accent colors around the MLPLAY wordmark. Colors follow the Cagecraft
dark theme.
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = Path(__file__).resolve().parent
BUNGEE = str(HERE / "fonts/Bungee-Regular.ttf")
NUNITO = str(HERE / "fonts/Nunito-SemiBold.ttf")

BG = (26, 29, 36)
BG_LIGHT = (40, 45, 56)
TEXT = (232, 234, 237)
MUTED = (154, 163, 178)
BLUE = (91, 143, 212)
BLUE_DARK = (58, 101, 160)
ACCENTS = [BLUE, (232, 138, 138), (126, 196, 150), (236, 196, 110), (170, 140, 220)]


def ml_tile(size: int) -> Image.Image:
    """A blue rounded tile with a white ML, drawn at 4x and scaled down."""
    s = size * 4
    img = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = s // 5
    d.rounded_rectangle((0, s // 24, s - 1, s - 1), r, fill=BLUE_DARK)
    d.rounded_rectangle((0, 0, s - 1, s - s // 24), r, fill=BLUE)
    font = ImageFont.truetype(BUNGEE, int(s * 0.46))
    box = d.textbbox((0, 0), "ML", font=font)
    x = (s - (box[2] - box[0])) / 2 - box[0]
    y = (s - s // 24 - (box[3] - box[1])) / 2 - box[1]
    d.text((x, y), "ML", font=font, fill=TEXT)
    return img.resize((size, size), Image.LANCZOS)


def make_icon() -> None:
    size = 512
    img = Image.new("RGBA", (size, size), BG + (255,))
    # Play may crop the icon to a circle: keep the tile inside it.
    tile = ml_tile(300)
    img.alpha_composite(tile, ((size - 300) // 2, (size - 300) // 2))
    img.save(HERE / "developer_icon.png")


def make_header() -> None:
    w, h = 4096, 2304
    img = Image.new("RGB", (w, h), BG)
    # Soft light from the middle.
    glow = Image.new("L", (w, h), 0)
    ImageDraw.Draw(glow).ellipse((w * 0.2, h * 0.1, w * 0.8, h * 0.9), fill=255)
    glow = glow.filter(ImageFilter.GaussianBlur(500))
    img = Image.composite(Image.new("RGB", (w, h), BG_LIGHT), img, glow)

    # Tiles on a loose grid, fading out toward the wordmark in the middle.
    rng = random.Random(7)
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    step = 256
    for gy in range(-1, h // step + 2):
        for gx in range(-1, w // step + 2):
            if rng.random() < 0.45:
                continue
            cx = gx * step + step / 2 + rng.uniform(-30, 30)
            cy = gy * step + step / 2 + rng.uniform(-30, 30)
            dx = (cx - w / 2) / (w * 0.36)
            dy = (cy - h / 2) / (h * 0.30)
            dist = (dx * dx + dy * dy) ** 0.5
            if dist < 1.0:
                continue
            alpha = int(min(1.0, (dist - 1.0) / 0.9) * rng.uniform(0.25, 0.75) * 255)
            color = rng.choice(ACCENTS) if rng.random() < 0.35 else (70, 78, 94)
            half = rng.choice([70, 85, 100])
            d.rounded_rectangle((cx - half, cy - half, cx + half, cy + half), half // 3, fill=color + (alpha,))
    img = Image.alpha_composite(img.convert("RGBA"), layer)

    # Wordmark: ML tile, then PLAY, with a line under it.
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(BUNGEE, 440)
    tile_size = 520
    gap = 60
    box = d.textbbox((0, 0), "PLAY", font=font)
    text_w = box[2] - box[0]
    total = tile_size + gap + text_w
    x0 = (w - total) // 2
    y0 = h // 2 - tile_size // 2 - 110
    img.alpha_composite(ml_tile(tile_size), (x0, y0))
    tx = x0 + tile_size + gap - box[0]
    ty = y0 + (tile_size - tile_size // 24 - (box[3] - box[1])) / 2 - box[1]
    d.text((tx, ty), "PLAY", font=font, fill=TEXT)

    sub = ImageFont.truetype(NUNITO, 150)
    line = "Games for Android"
    sb = d.textbbox((0, 0), line, font=sub)
    d.text(((w - (sb[2] - sb[0])) / 2 - sb[0], y0 + tile_size + 120), line, font=sub, fill=MUTED)

    out = HERE / "developer_header.jpg"
    img.convert("RGB").save(out, quality=90, optimize=True)


if __name__ == "__main__":
    make_icon()
    make_header()
