#!/usr/bin/env python3
"""
qr_gen.py — Portfolio QR Code Generator
Generates a professionally styled QR code card matching
the Nothing-inspired color scheme of r.sreesaran's portfolio.

Usage:
    python3 qr_gen.py

Dependencies:
    pip install "qrcode[pil]" Pillow
"""

import qrcode
from PIL import Image, ImageDraw, ImageFont
import sys
import os

# ── THEME DEFINITIONS ─────────────────────────────────────────────────────────
# Mirrors the CSS variables from style.css exactly
THEMES = {
    "ink": {
        "name":    "ink — light red",
        "bg":      (255, 255, 255),   # --bg
        "surface": (255, 248, 248),   # --surface
        "modules": (204,   0,   0),   # --heading / --accent  #CC0000
        "border":  (240, 224, 224),   # --border
        "text":    ( 26,  26,  26),   # --body
        "muted":   (176, 160, 160),   # --muted
        "accent":  (204,   0,   0),   # --accent
    },
    "void": {
        "name":    "void — dark mono",
        "bg":      ( 10,  10,  10),
        "surface": ( 18,  18,  18),
        "modules": (240, 240, 240),
        "border":  ( 28,  28,  28),
        "text":    (200, 200, 200),
        "muted":   ( 80,  80,  80),
        "accent":  (240, 240, 240),
    },
    "signal": {
        "name":    "signal — dark red",
        "bg":      ( 10,  10,  10),
        "surface": ( 20,   8,   8),
        "modules": (255,  48,  64),   # #FF3040
        "border":  ( 58,  16,  16),
        "text":    (200, 200, 200),
        "muted":   ( 80,  80,  80),
        "accent":  (255,  48,  64),
    },
    "paper": {
        "name":    "paper — light mono",
        "bg":      (255, 255, 255),
        "surface": (245, 245, 245),
        "modules": ( 10,  10,  10),
        "border":  (224, 224, 224),
        "text":    ( 61,  61,  61),
        "muted":   (176, 176, 176),
        "accent":  ( 10,  10,  10),
    },
}

# ── CARD DIMENSIONS ───────────────────────────────────────────────────────────
CARD_W      = 800
CARD_H      = 960
PADDING     = 64
QR_SIZE     = 560
DOT_SPACING = 22
DOT_RADIUS  = 1.2

# ── FONT HELPER ───────────────────────────────────────────────────────────────
def load_font(size, bold=False):
    """Try common system mono fonts, fall back to PIL default."""
    candidates = [
        "/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
        "/usr/share/fonts/TTF/DejaVuSansMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",             # macOS
        "C:/Windows/Fonts/consola.ttf",                # Windows
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

# ── DOT GRID BACKGROUND ───────────────────────────────────────────────────────
def draw_dot_grid(draw, width, height, dot_color, spacing=DOT_SPACING, radius=DOT_RADIUS):
    """Draw a subtle dot-matrix grid matching the website banner."""
    r = int(radius)
    for x in range(0, width, spacing):
        for y in range(0, height, spacing):
            draw.ellipse([x - r, y - r, x + r, y + r], fill=dot_color)

# ── MAIN GENERATOR ────────────────────────────────────────────────────────────
def generate_qr_card(url: str, theme_key: str = "ink", output_path: str = "qr_output.png"):
    t = THEMES[theme_key]

    # ── 1. Build raw QR ──────────────────────────────────────────────────────
    qr = qrcode.QRCode(
        version=None,             # auto-size
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # 30% recovery — best quality
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        fill_color=t["modules"],
        back_color=t["bg"],
    ).convert("RGBA")

    # Resize to target QR_SIZE
    qr_img = qr_img.resize((QR_SIZE, QR_SIZE), Image.NEAREST)

    # ── 2. Create card canvas ────────────────────────────────────────────────
    card = Image.new("RGB", (CARD_W, CARD_H), t["bg"])
    draw = ImageDraw.Draw(card)

    # Subtle dot-grid background (very faint — matches --border color at low alpha)
    dot_color = tuple(
        int(c * 0.4 + t["bg"][i] * 0.6)
        for i, c in enumerate(t["border"])
    )
    draw_dot_grid(draw, CARD_W, CARD_H, dot_color)

    # ── 3. Top label — name ──────────────────────────────────────────────────
    font_name  = load_font(36)
    font_small = load_font(20)
    font_tiny  = load_font(16)

    name_text = "r.sreesaran"
    name_bbox = draw.textbbox((0, 0), name_text, font=font_name)
    name_w    = name_bbox[2] - name_bbox[0]
    name_x    = (CARD_W - name_w) // 2
    name_y    = PADDING

    draw.text((name_x, name_y), name_text, fill=t["text"], font=font_name)

    # Role line below name
    role_text = "developer · student · bangalore"
    role_bbox = draw.textbbox((0, 0), role_text, font=font_small)
    role_w    = role_bbox[2] - role_bbox[0]
    role_x    = (CARD_W - role_w) // 2
    role_y    = name_y + (name_bbox[3] - name_bbox[1]) + 10

    draw.text((role_x, role_y), role_text, fill=t["accent"], font=font_small)

    # ── 4. Thin divider line under header ────────────────────────────────────
    div_y = role_y + (role_bbox[3] - role_bbox[1]) + 28
    draw.line([(PADDING, div_y), (CARD_W - PADDING, div_y)], fill=t["border"], width=1)

    # ── 5. Paste QR code centred ─────────────────────────────────────────────
    qr_x = (CARD_W - QR_SIZE) // 2
    qr_y = div_y + 32
    card.paste(qr_img, (qr_x, qr_y))

    # ── 6. QR border frame (1px) ─────────────────────────────────────────────
    draw.rectangle(
        [qr_x - 1, qr_y - 1, qr_x + QR_SIZE, qr_y + QR_SIZE],
        outline=t["border"],
        width=1,
    )

    # ── 7. URL text below QR ─────────────────────────────────────────────────
    url_y    = qr_y + QR_SIZE + 28
    url_disp = url if len(url) <= 48 else url[:45] + "…"
    url_bbox = draw.textbbox((0, 0), url_disp, font=font_tiny)
    url_w    = url_bbox[2] - url_bbox[0]
    url_x    = (CARD_W - url_w) // 2

    draw.text((url_x, url_y), url_disp, fill=t["muted"], font=font_tiny)

    # ── 8. Bottom bar — accent line + theme label ─────────────────────────────
    bottom_y = CARD_H - PADDING
    line_len  = 48

    draw.line(
        [(PADDING, bottom_y), (PADDING + line_len, bottom_y)],
        fill=t["accent"],
        width=2,
    )

    theme_label = f"portfolio 2025  ·  {t['name']}"
    draw.text((PADDING + line_len + 14, bottom_y - 8), theme_label, fill=t["muted"], font=font_tiny)

    # ── 9. Outer card border ──────────────────────────────────────────────────
    draw.rectangle([0, 0, CARD_W - 1, CARD_H - 1], outline=t["border"], width=1)

    # ── 10. Save ──────────────────────────────────────────────────────────────
    card.save(output_path, "PNG", dpi=(300, 300))
    print(f"\n  ✓ saved → {output_path}  ({CARD_W}×{CARD_H}px, 300dpi)\n")

# ── CLI ───────────────────────────────────────────────────────────────────────
def main():
    print("\n  ┌─────────────────────────────────────────┐")
    print("  │   qr_gen.py — portfolio qr generator    │")
    print("  └─────────────────────────────────────────┘\n")

    keys = list(THEMES.keys())

    # Accept URL (and optionally theme) as command-line args:
    #   python3 qr_gen.py https://sharanfr.github.io
    #   python3 qr_gen.py https://sharanfr.github.io void
    if len(sys.argv) >= 2:
        url = sys.argv[1].strip()
        print(f"  url      → {url}")
        theme_key = sys.argv[2].strip().lower() if len(sys.argv) >= 3 and sys.argv[2].lower() in keys else None
    else:
        url = input("  paste your website url → ").strip()
        theme_key = None

    if not url:
        print("  error: no url provided."); sys.exit(1)
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # Theme selection
    if theme_key is None:
        print("\n  choose a theme:")
        for i, k in enumerate(keys, 1):
            print(f"    {i}. {k:8s} — {THEMES[k]['name']}")
        choice = input(f"\n  enter 1–{len(keys)} [default: 1 / ink] → ").strip()
        try:
            theme_key = keys[int(choice) - 1] if choice else "ink"
        except (ValueError, IndexError):
            theme_key = "ink"
    else:
        print(f"  theme    → {theme_key}")

    out_name = f"qr_{theme_key}.png"
    # Output next to this script — always in tools/
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), out_name)

    print(f"\n  generating [{THEMES[theme_key]['name']}] …")
    generate_qr_card(url, theme_key, out_path)

if __name__ == "__main__":
    main()
