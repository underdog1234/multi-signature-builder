"""Regenerate the email-size logo PNGs used by the signature builder.

Reads the official Multi logo PNGs (transparent, 3400-4500 px wide) and writes
email-size versions into logos/. Each output is a flat palette colour with the
official logo's alpha channel, so the background is fully transparent. Sizes
are 4x the size the signature displays them at, so they stay sharp on retina
screens while staying small for email.

Usage:
    python tools/make_logos.py "<...>/01_Logos/For Screen"

Needs Pillow:  pip install pillow
"""
import sys
from collections import Counter
from pathlib import Path

from PIL import Image

# Palette hex values come from "Multi Colour Palette.pdf".
HEX = {
    "red": "#FF6354",         # Multi Red
    "warm-grey": "#E6E1DB",
    "blue": "#5298FE",
    "yellow": "#F3F4A8",
    "deep-red": "#60153B",
    "purple": "#CEC9FF",
    "white": "#FFFFFF",
    "light-grey": "#F5F3F3",
    "charcoal": "#575757",
    "warm-black": "#242424",
}

# The official "Grey" / "Black" files are the palette's Light Grey / Warm Black.
WORDMARK_FILES = {
    "red": "Red", "warm-grey": "Warm Grey", "blue": "Blue", "yellow": "Yellow",
    "deep-red": "Deep Red", "purple": "Purple", "white": "White",
    "light-grey": "Grey", "charcoal": "Charcoal", "warm-black": "Black",
}
LOCKUP_COLOURS = ["red", "warm-grey", "white", "light-grey", "charcoal", "warm-black"]


def lockup_files(kind):
    names = {"red": "Red", "warm-grey": "WarmGrey", "white": "White",
             "light-grey": "Grey", "charcoal": "Charcoal", "warm-black": "Black"}
    if kind == "Heritage":
        names["warm-grey"] = "Warm Grey"
    return names


# style -> (source sub-folder, source file template, output prefix, output size, colour files)
STYLES = {
    "wordmark": ("Primary Logo/PNG", "Multi_Logo_{c}.png", "multi-logo", (1040, 292), WORDMARK_FILES),
    "heritage": ("Lockups/PNG", "Multi_Logo_Heritage Lockup_{c}.png", "heritage-lockup", (1040, 380), lockup_files("Heritage")),
    "company": ("Lockups/PNG", "Multi_Logo_Company Lockup_{c}.png", "company-lockup", (1760, 373), lockup_files("Company")),
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    root = Path(sys.argv[1])
    out_dir = Path(__file__).resolve().parent.parent / "logos"
    out_dir.mkdir(exist_ok=True)

    for style, (folder, template, prefix, size, files) in STYLES.items():
        for slug, label in files.items():
            src = Image.open(root / folder / template.format(c=label)).convert("RGBA")

            # Sanity check: the official file should already be the palette colour.
            small = src.resize((200, 60))
            px = small.load()
            solid = Counter(px[x, y][:3] for y in range(60) for x in range(200) if px[x, y][3] == 255)
            if solid:
                found = "#%02X%02X%02X" % solid.most_common(1)[0][0]
                if found != HEX[slug]:
                    print(f"  warning: {style}/{slug} source is {found}, palette says {HEX[slug]}")

            alpha = src.getchannel("A").resize(size, Image.LANCZOS)
            out = Image.new("RGBA", size, hex_to_rgb(HEX[slug]) + (255,))
            out.putalpha(alpha)
            target = out_dir / f"{prefix}-{slug}.png"
            out.save(target, optimize=True)
            print(f"{target.name:34} {HEX[slug]}  {size[0]}x{size[1]}  {target.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
