"""One-off generator for real PNG app icons matching the Neurosonic brand
(dark background #060b14, cyan->violet gradient accent, bold "N" mark).

These replace the inline SVG data-URI icons in manifest.webmanifest, which
Android/TWA tooling (and some PWA installability checks) reject for launcher
icons. Run this script again if the brand mark changes; it is not part of
the runtime application, just a design asset generator.

Usage: python scripts/android/generate_icons.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "icons"

BG = (6, 11, 20, 255)          # #060b14
CYAN = (76, 201, 240, 255)     # #4cc9f0
VIOLET = (139, 92, 246, 255)   # #8b5cf6
WHITE = (237, 242, 255, 255)   # #edf2ff


def _lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def _gradient_disc(size: int, margin_ratio: float) -> Image.Image:
    """Circle filled with a diagonal cyan->violet gradient, transparent outside."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    margin = size * margin_ratio
    radius = size / 2 - margin
    cx = cy = size / 2
    for y in range(size):
        for x in range(size):
            dx, dy = x - cx, y - cy
            if dx * dx + dy * dy <= radius * radius:
                t = (x + y) / (2 * size)
                px[x, y] = (
                    _lerp(CYAN[0], VIOLET[0], t),
                    _lerp(CYAN[1], VIOLET[1], t),
                    _lerp(CYAN[2], VIOLET[2], t),
                    255,
                )
    return img


def _load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "segoeuib.ttf",
        "arialbd.ttf",
        "DejaVuSans-Bold.ttf",
    ]
    for name in candidates:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def make_icon(size: int, margin_ratio: float, out_path: Path) -> None:
    canvas = Image.new("RGBA", (size, size), BG)
    disc = _gradient_disc(size, margin_ratio)
    canvas.alpha_composite(disc)

    draw = ImageDraw.Draw(canvas)
    font = _load_font(int(size * 0.42))
    text = "N"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]),
        text, font=font, fill=WHITE,
    )

    canvas.convert("RGB").save(out_path, "PNG")
    print(f"wrote {out_path.relative_to(ROOT)} ({size}x{size})")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    # "any" purpose icons: content can touch the edges.
    make_icon(192, margin_ratio=0.06, out_path=OUT_DIR / "icon-192.png")
    make_icon(512, margin_ratio=0.06, out_path=OUT_DIR / "icon-512.png")
    # "maskable" icon: keep the visual inside the safe zone (~80% of canvas)
    # per https://web.dev/articles/maskable-icon, so OS masks don't crop it.
    make_icon(512, margin_ratio=0.22, out_path=OUT_DIR / "icon-512-maskable.png")


if __name__ == "__main__":
    main()
