"""Draw the front page of THE WORLD TODAY for Monday 23 November 2026.

Deterministic: fixed fonts, fixed coordinates, no randomness, no clock,
no network. Renders a 1024x1024 PNG with Pillow and writes it next to
this file as news_image.png. Run: python3 render.py
"""

from PIL import Image, ImageDraw, ImageFont

SIDE = 1024
EDGE = 36
INNER = SIDE - 2 * EDGE  # 952 px of content

PAPER = (248, 244, 234)
INK = (20, 20, 20)
FAINT = (118, 108, 92)
SOFT = (92, 86, 74)
CRIMSON = (176, 32, 32)
MIDNIGHT = (14, 24, 46)
OCEAN = (44, 90, 126)
SAND = (214, 162, 46)
LEAF = (72, 138, 72)
SMOKE = (120, 116, 108)
EMBER = (226, 92, 32)

FONTS = "/usr/share/fonts/truetype/dejavu/"
SERIF = FONTS + "DejaVuSerif.ttf"
SERIF_BOLD = FONTS + "DejaVuSerif-Bold.ttf"
SANS = FONTS + "DejaVuSans.ttf"
SANS_BOLD = FONTS + "DejaVuSans-Bold.ttf"


def face(path, size):
    return ImageFont.truetype(path, size)


def text_wrap(draw, words, fnt, width):
    """Break a string into lines that fit width pixels."""
    out = []
    for chunk in words.split("\n"):
        parts = chunk.split()
        if not parts:
            out.append("")
            continue
        line = parts[0]
        for word in parts[1:]:
            test = line + " " + word
            if draw.textlength(test, font=fnt) <= width:
                line = test
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def block(draw, x, y, words, fnt, width, step, colour=INK):
    """Draw a wrapped block of text; return the y just below it."""
    for line in text_wrap(draw, words, fnt, width):
        draw.text((x, y), line, font=fnt, fill=colour)
        y += step
    return y


def banner(draw, x, y, words, size, width, step=None):
    """Draw a bold serif headline; return the y just below it."""
    fnt = face(SERIF_BOLD, size)
    step = step or int(size * 1.1)
    return block(draw, x, y, words, fnt, width, step)


def tag(draw, x, y, words, width, colour=CRIMSON):
    """Section label in small caps with a hairline under it."""
    fnt = face(SANS_BOLD, 15)
    draw.text((x, y), words.upper(), font=fnt, fill=colour)
    y += 22
    draw.line([(x, y), (x + width, y)], fill=FAINT, width=1)
    return y + 8


def rule_across(draw, y, weight=2):
    draw.line([(EDGE, y), (SIDE - EDGE, y)], fill=INK, width=weight)
    return y + weight


def art_box(canvas, scene, x, y, w, h):
    """Paint a scene on its own layer, clipped to its box."""
    layer = Image.new("RGB", (w, h), PAPER)
    pen = ImageDraw.Draw(layer)
    scene(pen, 0, 0, w, h)
    canvas.paste(layer, (x, y))


def summit_scene(pen, x, y, w, h):
    """The Antalya hall at dusk: a setting sun, a cracked globe, empty chairs."""
    pen.rectangle([x, y, x + w, y + h], fill=(238, 228, 208))
    # low sun, half set
    cx = x + w // 2
    pen.ellipse([cx - 40, y + 6, cx + 40, y + 86], fill=SAND)
    # globe below the sun, cracked
    gx, gy = cx - 30, y + 48
    pen.ellipse([gx, gy, gx + 60, gy + 60], fill=OCEAN)
    pen.polygon([(gx + 10, gy + 12), (gx + 26, gy + 22), (gx + 20, gy + 34),
                 (gx + 36, gy + 26), (gx + 28, gy + 44), (gx + 42, gy + 38),
                 (gx + 38, gy + 18)], fill=LEAF)
    pen.line([(gx + 6, gy + 26), (gx + 24, gy + 38), (gx + 18, gy + 50),
              (gx + 38, gy + 46)], fill=(248, 244, 234), width=3)
    pen.text((x + 10, y + h - 18),
             "The closing plenary in Antalya: no consensus, no pact.",
             font=face(SANS, 12), fill=INK)


def fire_scene(pen, x, y, w, h):
    """A factory block with flames and smoke columns."""
    pen.rectangle([x, y, x + w, y + h], fill=(232, 222, 206))
    for sx, sy, r in [(90, 14, 14), (130, 6, 18), (300, 10, 16),
                      (340, 20, 12), (400, 8, 14)]:
        pen.ellipse([x + sx - r, y + sy - r // 2, x + sx + r, y + sy + r],
                    fill=SMOKE)
    bx, by = x + 60, y + h - 28
    pen.rectangle([bx, by, bx + 220, y + h], fill=(70, 60, 52))
    pen.rectangle([bx + 230, by + 10, bx + 300, y + h], fill=(70, 60, 52))
    for fx in (bx + 30, bx + 110, bx + 190, bx + 258):
        pen.polygon([(fx, by), (fx + 14, by - 24), (fx + 28, by)],
                    fill=EMBER)
        pen.polygon([(fx + 7, by), (fx + 14, by - 12), (fx + 21, by)],
                    fill=(255, 220, 120))


def quake_scene(pen, x, y, w, h):
    """Andean ridge split by a crack, one house tilted."""
    pen.rectangle([x, y, x + w, y + h], fill=(240, 234, 216))
    pen.polygon([(x, y + h), (x, y + 34), (x + 140, y + 14),
                 (x + 280, y + 38), (x + w, y + 20), (x + w, y + h)],
                fill=(96, 84, 66))
    pen.line([(x + 220, y + 20), (x + 236, y + 40), (x + 224, y + 56),
              (x + 244, y + h - 8)], fill=INK, width=3)
    hx, hy = x + 60, y + h - 30
    pen.rectangle([hx + 8, hy + 6, hx + 60, hy + 16], fill=(240, 234, 216))
    pen.polygon([(hx, hy + 6), (hx + 34, hy - 10), (hx + 68, hy + 6)],
                fill=CRIMSON)
    pen.text((x + 12, y + 6), "Junin, Peru  ·  magnitude 6.7",
             font=face(SANS_BOLD, 12), fill=INK)


def drone_scene(pen, x, y, w, h):
    """A five-storey block, smoke from a hit floor, a drone above."""
    pen.rectangle([x, y, x + w, y + h], fill=(226, 224, 214))
    bx, by = x + 40, y + 12
    pen.rectangle([bx, by, bx + 150, y + h], fill=(88, 84, 76))
    for r in range(4):
        for c in range(3):
            pen.rectangle([bx + 14 + c * 44, by + 10 + r * 14,
                           bx + 34 + c * 44, by + 20 + r * 14],
                          fill=(210, 206, 196))
    pen.ellipse([bx + 96, by - 2, bx + 150, by + 22], fill=SMOKE)
    pen.ellipse([bx + 116, by - 8, bx + 158, by + 10], fill=(160, 156, 148))
    pen.ellipse([x + w - 26, y + 6, x + w - 14, y + 18], fill=INK)
    pen.line([(x + w - 34, y + 12), (x + w - 6, y + 12)], fill=INK, width=2)


def ship_scene(pen, x, y, w, h):
    """A cargo ship burning on a grey Baltic sea."""
    pen.rectangle([x, y, x + w, y + h], fill=(214, 222, 228))
    pen.rectangle([x, y + h - 16, x + w, y + h], fill=OCEAN)
    pen.rectangle([x + 40, y + h - 30, x + w - 40, y + h - 16],
                  fill=(52, 48, 44))
    pen.rectangle([x + 120, y + h - 46, x + 170, y + h - 30],
                  fill=(52, 48, 44))
    pen.polygon([(x + 138, y + h - 46), (x + 152, y + h - 70),
                 (x + 168, y + h - 46)], fill=EMBER)
    pen.polygon([(x + 145, y + h - 46), (x + 152, y + h - 58),
                 (x + 161, y + h - 46)], fill=(255, 220, 120))
    for sx, sy, r in [(150, 8, 10), (176, 4, 12), (200, 12, 9)]:
        pen.ellipse([x + sx - r, y + sy, x + sx + r, y + sy + r],
                    fill=SMOKE)


def tanker_scene(pen, x, y, w, h):
    """Two tankers in a strait, a projectile arc overhead."""
    pen.rectangle([x, y, x + w, y + h], fill=(206, 224, 232))
    pen.rectangle([x, y + h - 18, x + w, y + h], fill=OCEAN)
    for tx in (30, 170):
        pen.rectangle([x + tx, y + h - 32, x + tx + 100, y + h - 18],
                      fill=(70, 60, 50))
        pen.ellipse([x + tx + 20, y + h - 44, x + tx + 40, y + h - 32],
                    fill=(180, 180, 170))
    pen.arc([x + 90, y + 2, x + 210, y + 34], start=200, end=340,
            fill=EMBER, width=3)
    pen.ellipse([x + 198, y + 24, x + 210, y + 36], fill=EMBER)
    for dx, dy in [(-8, -8), (0, -10), (8, -8)]:
        pen.line([(x + 204, y + 30), (x + 204 + dx, y + 30 + dy)],
                 fill=(255, 255, 255), width=2)


def front_page():
    img = Image.new("RGB", (SIDE, SIDE), PAPER)
    pen = ImageDraw.Draw(img)

    # ---- masthead ----
    pen.text((EDGE, 16), "THE WORLD TODAY", font=face(SERIF_BOLD, 60),
             fill=INK)
    y = 90
    y = rule_across(pen, y, 3)
    y += 6
    line = "MONDAY, 23 NOVEMBER 2026  ·  ONE DAY'S WORLD NEWS IN ONE PAGE"
    pen.text((EDGE, y), line, font=face(SANS_BOLD, 17), fill=INK)
    no = "No. 328"
    pen.text((SIDE - EDGE - pen.textlength(no, font=face(SANS_BOLD, 17)), y),
             no, font=face(SANS_BOLD, 17), fill=INK)
    y += 28
    y = rule_across(pen, y, 1)

    # ---- lead story ----
    y += 8
    y = banner(pen, EDGE, y, "CLIMATE TALKS COLLAPSE IN ANTALYA", 44, INNER)
    y += 2
    y = block(pen, EDGE, y,
              "No deal after the longest COP in history; EU rejects a pact that never names fossil fuels",
              face(SERIF, 20), INNER, 26, SOFT)
    y += 8
    art_box(img, summit_scene, EDGE, y, INNER, 118)
    y += 118 + 6
    half_w = (INNER - 24) // 2
    left = ("United Nations climate talks in Antalya collapsed on Sunday "
            "after more than two weeks of negotiation, the first breakdown "
            "since Copenhagen in 2009. The EU, Panama, the Marshall "
            "Islands and Norway rejected the Antalya Pact.")
    right = ("The draft never mentioned fossil fuels and dropped a $120bn "
             "adaptation-finance target. UN chief Antonio Guterres said he "
             "was deeply disappointed, accusing fossil-fuel interests of "
             "obstructing action while the planet warms.")
    y1 = block(pen, EDGE, y, left, face(SERIF, 15), half_w, 19)
    y2 = block(pen, EDGE + half_w + 24, y, right, face(SERIF, 15), half_w, 19)
    y = max(y1, y2) + 6
    y = rule_across(pen, y, 1)
    y += 8

    # ---- middle row: Indonesia fire + Peru quake ----
    y_top = y
    y = tag(pen, EDGE, y, "Disaster · Indonesia", half_w)
    y = banner(pen, EDGE, y, "FACTORY FIRE: 3 DEAD, 36 MISSING", 24, half_w, 26)
    y = block(pen, EDGE, y + 4,
              "A fire tore through the Fonusa Agung Mulia candy factory in "
              "Banten, west of Jakarta. Fifty-four workers were first "
              "unaccounted for; 15 were rescued and the search goes on.",
              face(SERIF, 14), half_w, 17)
    art_box(img, fire_scene, EDGE, y + 6, half_w, 64)
    left_end = y + 6 + 64
    yr = tag(pen, EDGE + half_w + 24, y_top, "Disaster · Peru", half_w)
    yr = banner(pen, EDGE + half_w + 24, yr, "6.7 QUAKE SHAKES THE ANDES",
                24, half_w, 26)
    yr = block(pen, EDGE + half_w + 24, yr + 4,
               "A magnitude 6.7 earthquake struck near Junin on Friday "
               "evening, killing 1, injuring 16, damaging more than 150 "
               "houses and cutting power for nearly 93,000 people.",
               face(SERIF, 14), half_w, 17)
    art_box(img, quake_scene, EDGE + half_w + 24, yr + 6, half_w, 64)
    y = max(left_end, yr + 6 + 64) + 6
    y = rule_across(pen, y, 1)
    y += 8

    # ---- bottom row: three tiles ----
    third = (INNER - 48) // 3
    xs = [EDGE, EDGE + third + 24, EDGE + 2 * (third + 24)]
    tiles = [
        ("War · Ukraine", "DRONE HITS FLAT, 14 MISSING",
         "A Russian drone struck a five-storey apartment block in Dymer, "
         "near Kyiv, leaving at least 14 people missing.",
         drone_scene),
        ("Baltic · Sea", "CARGO SHIP STILL BURNING",
         "A Russian cargo ship was still on fire off Finland after a "
         "drone attack; Helsinki tightened security.",
         ship_scene),
        ("Gulf · Hormuz", "TANKERS STRUCK IN STRAIT",
         "At least two oil tankers were hit by projectiles in the Strait "
         "of Hormuz amid tensions with Iran.",
         tanker_scene),
    ]
    y_top = y
    y_bottom = y_top
    for (kick, head, body, scene), x in zip(tiles, xs):
        yy = tag(pen, x, y_top, kick, third)
        yy = banner(pen, x, yy, head, 20, third, 22)
        yy = block(pen, x, yy + 4, body, face(SERIF, 13), third, 16)
        art_box(img, scene, x, yy + 6, third, 48)
        y_bottom = max(y_bottom, yy + 6 + 48)
    y = y_bottom + 8
    y = rule_across(pen, y, 1)
    y += 6

    # ---- briefs ----
    pen.text((EDGE, y), "IN BRIEF", font=face(SANS_BOLD, 15), fill=CRIMSON)
    y += 22
    briefs = [
        "G20 opens in Johannesburg, the first summit on African soil.",
        "Myanmar calls an ASEAN decision 'unfair and imbalanced'.",
        "Thousands march in Lisbon as living costs fuel anger.",
        "South Korea's education chief quits in AI cheating scandal.",
        "BepiColombo spacecraft reaches the planet Mercury.",
        "Nepal PM Balen Shah in India for talks with Prime Minister Modi.",
    ]
    fnt = face(SERIF, 13)
    row = 17
    for i, item in enumerate(briefs):
        bx = EDGE if i % 2 == 0 else EDGE + half_w + 24
        by = y + (i // 2) * row
        pen.text((bx, by), "•  " + item, font=fnt, fill=INK)
    y = y + ((len(briefs) + 1) // 2) * row + 4
    y = rule_across(pen, y, 1)

    # ---- footer ----
    pen.text((EDGE, y + 8),
             "THE WORLD TODAY  ·  Monday, 23 November 2026  ·  Sources: CNN, Le Monde, Nikkei, Al Jazeera, AFP",
             font=face(SANS, 13), fill=SOFT)

    img.save("news_image.png")
    print("wrote news_image.png", img.size, "final y:", y)


if __name__ == "__main__":
    front_page()
