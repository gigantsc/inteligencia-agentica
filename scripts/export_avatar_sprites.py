#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporta sprites RGBA do avatar hermes-assistant em WebP otimizado (260x301)."""
import os
from PIL import Image

SRC_DIR = r"D:\DevCod\avatar\avatares\hermes-assistant"
OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static",
    "images",
    "avatar",
)
TARGET_SIZE = (260, 301)

SPRITE_MAP = {
    "fall-drop.webp": "falling-2-drop.png",
    "fall-land.webp": "falling-3-land.png",
    "fall-getup.webp": "falling-4-getup.png",
    "fall-dizzy.webp": "falling-5-dizzy.png",
    "wave-1.webp": "wave-1.png",
    "wave-2.webp": "wave-2.png",
    "wave-3.webp": "wave-3.png",
    "blink.webp": "eyes-blink.png",
}
for i in range(8):
    SPRITE_MAP[f"breathe-{i}.webp"] = f"breathe-{i}.png"
    SPRITE_MAP[f"talk-{i}.webp"] = f"talk-0-{i}.png"
    SPRITE_MAP[f"walk-left-{i}.webp"] = f"walk-left-{i}.png"
    SPRITE_MAP[f"walk-right-{i}.webp"] = f"walk-right-{i}.png"
for i in range(6):
    SPRITE_MAP[f"approve-{i}.webp"] = f"approve-{i}.png"


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    total_bytes = 0
    for out_name, src_name in sorted(SPRITE_MAP.items()):
        src_path = os.path.join(SRC_DIR, src_name)
        if not os.path.isfile(src_path):
            raise SystemExit(f"ERRO: sprite ausente: {src_path}")
        out_path = os.path.join(OUT_DIR, out_name)
        with Image.open(src_path) as im:
            rgba = im.convert("RGBA")
            resized = rgba.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
            resized.save(out_path, "WEBP", quality=82, method=6)
        size = os.path.getsize(out_path)
        total_bytes += size
        with Image.open(out_path) as check:
            assert check.size == TARGET_SIZE, f"{out_name} size={check.size}"
            assert check.mode == "RGBA", f"{out_name} mode={check.mode}"
    print(f"OK: {len(SPRITE_MAP)} sprites WebP RGBA ({TARGET_SIZE[0]}x{TARGET_SIZE[1]}), total {total_bytes / 1024:.1f} KB")


if __name__ == "__main__":
    main()
