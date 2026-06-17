# -*- coding: utf-8 -*-
"""產生狼人殺宣導站全套圖示：favicon.ico / favicon.svg(另外寫) / app icons / maskable。
主題：滿月 + 幾何狼頭剪影，深靛藍夜色。純 PIL 繪製，無外部字型依賴。"""
import math, os
from PIL import Image, ImageDraw, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
os.makedirs(ASSETS, exist_ok=True)

# 色票
NIGHT_TOP = (30, 27, 75)      # #1e1b4b
NIGHT_BOT = (49, 46, 129)     # #312e81
MOON_LIGHT = (253, 230, 138)  # #fde68a
MOON_DARK = (251, 191, 36)    # #fbbf24
WOLF = (10, 12, 30)           # 深夜藍黑
EYE = (252, 211, 77)          # 琥珀


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(size, top, bot):
    img = Image.new("RGB", (1, size))
    for y in range(size):
        img.putpixel((0, y), lerp(top, bot, y / max(1, size - 1)))
    return img.resize((size, size))


def rounded_mask(size, radius):
    m = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(m)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=radius, fill=255)
    return m


def wolf_head_points(cx, cy, scale):
    """正面幾何狼頭剪影，回傳多邊形座標 (以 100x100 基準設計後位移縮放)。"""
    pts = [
        (20, 6), (36, 28), (50, 22), (64, 28), (80, 6),
        (86, 34), (82, 53), (72, 67), (58, 79), (50, 86),
        (42, 79), (28, 67), (18, 53), (14, 34),
    ]
    out = []
    for x, y in pts:
        out.append((cx + (x - 50) * scale, cy + (y - 50) * scale))
    return out


def draw_icon(size, maskable=False):
    SS = 4  # 超取樣抗鋸齒
    S = size * SS
    base = vgrad(S, NIGHT_TOP, NIGHT_BOT).convert("RGBA")
    draw = ImageDraw.Draw(base)

    # 內容安全縮放：maskable 內縮到 ~78%
    content = 0.78 if maskable else 1.0
    cx, cy = S / 2, S / 2

    # 星點
    import random
    random.seed(7)
    for _ in range(int(26 * (S / 512))):
        x = random.randint(0, S - 1)
        y = random.randint(0, int(S * 0.55))
        r = random.choice([1, 1, 2]) * SS
        a = random.randint(60, 170)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(255, 255, 255, a))

    # 滿月（帶光暈）置中偏上
    moon_r = S * 0.37 * content
    mx, my = cx, cy - S * 0.02 * content
    glow = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([mx - moon_r * 1.5, my - moon_r * 1.5, mx + moon_r * 1.5, my + moon_r * 1.5],
               fill=(253, 230, 138, 70))
    glow = glow.filter(ImageFilter.GaussianBlur(S * 0.04))
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)

    # 月面漸層（手繪同心）
    steps = 60
    for i in range(steps, 0, -1):
        t = i / steps
        rr = moon_r * t
        col = lerp(MOON_DARK, MOON_LIGHT, 1 - t)
        draw.ellipse([mx - rr, my - rr, mx + rr, my + rr], fill=col + (255,))
    # 月坑
    for (ox, oy, orr) in [(-0.35, -0.25, 0.14), (0.30, 0.10, 0.10), (-0.05, 0.38, 0.08)]:
        cr = moon_r * orr
        draw.ellipse([mx + ox * moon_r - cr, my + oy * moon_r - cr,
                      mx + ox * moon_r + cr, my + oy * moon_r + cr],
                     fill=lerp(MOON_DARK, NIGHT_BOT, 0.25) + (90,))

    # 狼頭剪影（置於月面前，耳朵微突月緣）
    scale = (S / 100) * 0.98 * content
    wcx, wcy = mx, my + S * 0.02 * content
    pts = wolf_head_points(wcx, wcy, scale)
    draw.polygon(pts, fill=WOLF + (255,))

    # 眼睛（發光琥珀）
    eye_dx = 11 * scale
    eye_y = wcy - 4 * scale
    er = 3.6 * scale
    for sx in (-1, 1):
        ex = cx + sx * eye_dx
        # 杏仁形眼睛（菱形）
        draw.polygon([(ex, eye_y - er), (ex + er * 0.8, eye_y),
                      (ex, eye_y + er * 0.7), (ex - er * 0.8, eye_y)], fill=EYE + (255,))
    # 鼻子
    nose_y = wcy + 16 * scale
    nr = 3.0 * scale
    draw.polygon([(cx, nose_y + nr), (cx - nr, nose_y - nr * 0.6),
                  (cx + nr, nose_y - nr * 0.6)], fill=EYE + (220,))

    img = base.resize((size, size), Image.LANCZOS)

    if not maskable:
        mask = rounded_mask(size, int(size * 0.22))
        out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        out.paste(img, (0, 0), mask)
        return out
    return img.convert("RGBA")


# 產出
draw_icon(192).save(os.path.join(ASSETS, "icon-192.png"))
draw_icon(512).save(os.path.join(ASSETS, "icon-512.png"))
draw_icon(192, maskable=True).save(os.path.join(ASSETS, "icon-192-maskable.png"))
draw_icon(512, maskable=True).save(os.path.join(ASSETS, "icon-512-maskable.png"))
draw_icon(180).save(os.path.join(ROOT, "apple-touch-icon.png"))
# favicon.ico 多尺寸
ico = draw_icon(64)
ico.save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
# OG 預覽圖 1200x630
og = vgrad(1200, NIGHT_TOP, NIGHT_BOT).convert("RGBA")
icon_big = draw_icon(360, maskable=True)
og.alpha_composite(icon_big, (110, 135))
og.convert("RGB").save(os.path.join(ASSETS, "og-cover.png"))
print("icons generated ->", os.listdir(ASSETS))
