#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Exporta sprites RGBA do avatar hermes-assistant e compre_aqui.gif em WebP otimizado (260x301)."""
import os
from collections import deque
from PIL import Image, ImageSequence

SRC_DIR = r"D:\DevCod\avatar\avatares\hermes-assistant"
COMPREAQUI_GIF = r"D:\DevCod\mybrother_bit\assets\compre_aqui.gif"
OUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "static",
    "images",
    "avatar",
)
TARGET_SIZE = (260, 301)
CANVAS_SIZE = (1054, 1220)
CENTER_X = 528.5
BASELINE_Y = 1183
TARGET_H = 1131

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


def remove_black_background(frame: Image.Image, threshold: int = 2) -> Image.Image:
    """Remove fundo preto conectado às bordas via flood-fill BFS preservando o contorno."""
    width, height = frame.size
    pixels = frame.load()
    visited = bytearray(width * height)
    queue: deque[tuple[int, int]] = deque()

    def is_bg(x: int, y: int) -> bool:
        r, g, b, a = pixels[x, y]
        return a > 0 and r <= threshold and g <= threshold and b <= threshold

    for x in range(width):
        for y in (0, height - 1):
            if not visited[y * width + x] and is_bg(x, y):
                visited[y * width + x] = 1
                queue.append((x, y))
    for y in range(height):
        for x in (0, width - 1):
            if not visited[y * width + x] and is_bg(x, y):
                visited[y * width + x] = 1
                queue.append((x, y))

    while queue:
        x, y = queue.popleft()
        pixels[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < width and 0 <= ny < height and not visited[ny * width + nx] and is_bg(nx, ny):
                visited[ny * width + nx] = 1
                queue.append((nx, ny))
    return frame


def keep_largest_opaque_component(frame: Image.Image) -> Image.Image:
    """Mantém apenas o maior componente conexo opaco, removendo halos isolados nas bordas."""
    width, height = frame.size
    pixels = frame.load()
    visited = bytearray(width * height)
    largest: list[tuple[int, int]] = []
    components: list[list[tuple[int, int]]] = []

    for y in range(height):
        for x in range(width):
            if pixels[x, y][3] > 0 and not visited[y * width + x]:
                visited[y * width + x] = 1
                cq: deque[tuple[int, int]] = deque([(x, y)])
                pts: list[tuple[int, int]] = []
                while cq:
                    cx, cy = cq.popleft()
                    pts.append((cx, cy))
                    for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
                        if 0 <= nx < width and 0 <= ny < height and not visited[ny * width + nx]:
                            if pixels[nx, ny][3] > 0:
                                visited[ny * width + nx] = 1
                                cq.append((nx, ny))
                components.append(pts)
                if len(pts) > len(largest):
                    largest = pts

    for comp in components:
        if comp is not largest:
            for cx, cy in comp:
                pixels[cx, cy] = (0, 0, 0, 0)
    return frame


def export_compreaqui_frames() -> tuple[int, int]:
    """Exporta compre_aqui.gif como frames RGBA WebP (260x301) sem fundo preto."""
    if not os.path.isfile(COMPREAQUI_GIF):
        raise SystemExit(f"ERRO: GIF ausente: {COMPREAQUI_GIF}")

    cleaned_frames: list[Image.Image] = []
    with Image.open(COMPREAQUI_GIF) as gif:
        for frame in ImageSequence.Iterator(gif):
            rgba = frame.convert("RGBA").copy()
            no_bg = remove_black_background(rgba, threshold=2)
            cleaned_frames.append(keep_largest_opaque_component(no_bg))

    bbox0 = cleaned_frames[0].getbbox()
    if bbox0 is None:
        raise SystemExit("ERRO: frame 0 de compre_aqui.gif vazio após remoção de fundo")

    anchor_cx = (bbox0[0] + bbox0[2]) / 2.0
    scale = TARGET_H / float(bbox0[3] - bbox0[1])

    total_bytes = 0
    for idx, frame in enumerate(cleaned_frames):
        bbox = frame.getbbox()
        if bbox is None:
            raise SystemExit(f"ERRO: frame {idx} de compre_aqui.gif vazio")

        scaled_w = round(frame.width * scale)
        scaled_h = round(frame.height * scale)
        scaled = frame.resize((scaled_w, scaled_h), Image.Resampling.NEAREST)

        left = round(CENTER_X - scale * anchor_cx)
        top = round(BASELINE_Y - scale * bbox[3])

        canvas = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
        canvas.paste(scaled, (left, top), scaled)

        final_img = canvas.resize(TARGET_SIZE, Image.Resampling.LANCZOS)
        out_name = f"compreaqui-{idx}.webp"
        out_path = os.path.join(OUT_DIR, out_name)
        final_img.save(out_path, "WEBP", quality=82, method=6)
        total_bytes += os.path.getsize(out_path)

        with Image.open(out_path) as check:
            assert check.size == TARGET_SIZE, f"{out_name} size={check.size}"
            assert check.mode == "RGBA", f"{out_name} mode={check.mode}"
            cw, ch = check.size
            for cx, cy in ((0, 0), (cw - 1, 0), (0, ch - 1), (cw - 1, ch - 1)):
                assert check.getpixel((cx, cy))[3] == 0, f"{out_name} corner ({cx},{cy}) alpha != 0"

    return len(cleaned_frames), total_bytes


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

    compre_count, compre_bytes = export_compreaqui_frames()
    total_sprites = len(SPRITE_MAP) + compre_count
    total_kb = (total_bytes + compre_bytes) / 1024
    print(
        f"OK: {total_sprites} sprites WebP RGBA ({TARGET_SIZE[0]}x{TARGET_SIZE[1]}: "
        f"{len(SPRITE_MAP)} base + {compre_count} compreaqui), total {total_kb:.1f} KB"
    )


if __name__ == "__main__":
    main()
