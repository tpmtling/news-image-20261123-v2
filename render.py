#!/usr/bin/env python3
"""Front page of THE WORLD TODAY, No. 328 - Monday 23 November 2026.

Draws a 1024x1024 newspaper front page with Pillow from the story table
below (transcribed from news_data.md). No input files are read at run
time; the output is fully deterministic - the same run always writes the
same bytes.
"""

import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

CANVAS = (1024, 1024)
PAPER = (247, 242, 231)
INK = (18, 18, 18)
SOFT = (74, 70, 62)
RED = (178, 34, 28)
NAVY = (24, 42, 68)
SKY = (188, 214, 232)
SEA = (46, 92, 128)
LEAF = (74, 122, 66)
FLAME = (232, 100, 28)
GOLD = (214, 164, 32)

SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"


def face(path, size):
    """Load a TrueType face, falling back to Pillow's built-in bitmap."""
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.load_default()


class Faces:
    """All typefaces used on the page, loaded once."""

    def __init__(self):
        self.masthead = face(SERIF_BOLD, 80)
        self.headline = face(SERIF_BOLD, 47)
        self.card_head = face(SERIF_BOLD, 21)
        self.deck = face(SERIF, 20)
        self.body = face(SERIF, 18)
        self.card_body = face(SERIF, 15)
        self.brief = face(SANS, 14)
        self.brief_bold = face(SANS_BOLD, 14)
        self.kicker = face(SANS_BOLD, 16)
        self.small = face(SANS_BOLD, 15)
        self.tag = face(SANS, 15)
        self.quote = face(SERIF, 20)
        self.stamp = face(SANS_BOLD, 26)


FACES = Faces()


def wrap_text(pen, text, font, width):
    """Split text into lines that fit width, measured with the real font."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for word in words[1:]:
            trial = cur + " " + word
            if pen.textlength(trial, font=font) <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = word
        lines.append(cur)
    return lines


def spaced(pen, xy, text, font, fill, gap=2):
    """Draw text with extra tracking between letters; return width used."""
    x, y = xy
    total = 0
    for ch in text:
        pen.text((x, y), ch, font=font, fill=fill)
        step = pen.textlength(ch, font=font) + gap
        x += step
        total += step
    return total - gap if text else 0


def spaced_width(pen, text, font, gap=2):
    return sum(pen.textlength(c, font=font) + gap for c in text) - gap


def rule(pen, x0, x1, y, weight=2, fill=INK):
    pen.line([(x0, y), (x1, y)], fill=fill, width=weight)


def para(pen, x, y, width, text, font, fill=INK, leading=1.28):
    """Draw a wrapped paragraph; return the y just below its last line."""
    lines = wrap_text(pen, text, font, width)
    step = int(font.size * leading)
    for line in lines:
        pen.text((x, y), line, font=font, fill=fill)
        y += step
    return y


# ---------------------------------------------------------------- stories

LEAD_KICKER = "CLIMATE  ·  ANTALYA, TURKEY"
LEAD_HEAD = "COP31 COLLAPSES WITHOUT A DEAL"
LEAD_DECK = ("After more than two weeks of talks, no deal - the first "
             "UN climate breakdown since Copenhagen in 2009.")
LEAD_BODY = ("The EU, Panama, the Marshall Islands and Norway rejected the "
             "draft \u201cAntalya Pact\u201d because it never mentioned "
             "fossil fuels. The draft also dropped a $120bn adaptation "
             "target, in the longest COP in history. UN chief "
             "Ant\u00f3nio Guterres said he was deeply disappointed.")

CARDS = [
    dict(art="flame", kick="INDONESIA  ·  BANTEN",
         head="Factory fire kills 3, 36 missing",
         body=("Fire at the Fonusa Agung Mulia candy factory, west of "
               "Jakarta; 36 workers missing, 15 rescued.")),
    dict(art="quake", kick="PERU  ·  JUN\u00cdN",
         head="6.7 quake shakes the Andes",
         body=("One person was killed, 16 injured and 150 houses damaged; "
               "power was cut for nearly 93,000.")),
    dict(art="block", kick="UKRAINE  ·  NEAR KYIV",
         head="Drone hits flats in Dymer",
         body=("A Russian drone struck a five-storey apartment block; at "
               "least 14 people were missing.")),
    dict(art="ship", kick="THE BALTIC  ·  OFF FINLAND",
         head="Cargo ship still burning",
         body=("A Russian cargo ship was still on fire after a drone "
               "attack; Finland tightened security.")),
    dict(art="tanker", kick="STRAIT OF HORMUZ",
         head="Two tankers struck",
         body=("At least two oil tankers were hit by projectiles amid "
               "tensions involving Iran and the United States.")),
]

BRIEFS = [
    ("G20", "The summit opened in Johannesburg, the first ever held on "
            "African soil."),
    ("MYANMAR", "The army-backed government called an ASEAN decision "
                "\u201cunfair and imbalanced\u201d."),
    ("LISBON", "Thousands marched as the rising cost of living fuels anger."),
    ("SEOUL", "South Korea\u2019s education chief quit amid an AI "
              "exam-cheating scandal."),
    ("SPACE", "The BepiColombo spacecraft reached the planet Mercury."),
    ("NEW DELHI", "Nepal\u2019s PM Balen Shah began his first visit to India, "
                  "for talks with PM Modi."),
]

QUOTE_TEXT = ("\u201cDeeply disappointed.\u201d")
QUOTE_ATTR = ("UN chief Ant\u00f3nio Guterres\non the collapse of the talks")


# ---------------------------------------------------------------- pictures

def art_globe(pen, box):
    """A cracked globe with a NO DEAL stamp, for the lead panel."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2 - 8
    r = 92
    pen.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SKY, outline=INK,
                width=3)
    for lat in ((-56, 200, 340), (0, 200, 340), (56, 20, 160)):
        dy, a0, a1 = lat
        inset = 18 if dy else 0
        half = 20 if dy else 14
        pen.arc([cx - r + inset, cy + dy - half, cx + r - inset,
                 cy + dy + half], start=a0, end=a1, fill=SEA, width=2)
    for k in (-46, 0, 46):
        pen.arc([cx + k - 34, cy - r, cx + k + 34, cy + r],
                start=270, end=90, fill=SEA, width=2)
    pen.polygon([(cx - 62, cy - 30), (cx - 18, cy - 52), (cx + 6, cy - 26),
                 (cx - 8, cy + 2), (cx - 40, cy - 6)], fill=LEAF)
    pen.polygon([(cx + 12, cy + 28), (cx + 52, cy + 12), (cx + 66, cy + 44),
                 (cx + 30, cy + 62), (cx + 8, cy + 48)], fill=LEAF)
    crack = [(cx - 6, cy - r + 4), (cx + 14, cy - 58), (cx - 10, cy - 22),
             (cx + 18, cy + 12), (cx - 8, cy + 48), (cx + 10, cy + r - 6)]
    pen.line(crack, fill=RED, width=5, joint="curve")
    stamp = Image.new("RGBA", (210, 64), (0, 0, 0, 0))
    sp = ImageDraw.Draw(stamp)
    sp.rectangle([3, 3, 206, 60], outline=RED, width=4)
    sp.text((105, 32), "NO DEAL", font=FACES.stamp, fill=RED, anchor="mm")
    stamp = stamp.rotate(11, expand=True, resample=Image.BICUBIC)
    pen._image.paste(stamp, (x1 - 216, y1 - 80), stamp)


def art_flame(pen, box):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    pen.polygon([(cx - 26, y1 - 6), (cx - 30, y0 + 26), (cx - 12, y0 + 12),
                 (cx - 2, y0 + 2), (cx + 10, y0 + 18), (cx + 28, y0 + 30),
                 (cx + 24, y1 - 6)], fill=FLAME)
    pen.polygon([(cx - 12, y1 - 6), (cx - 10, y0 + 26), (cx + 2, y0 + 18),
                 (cx + 12, y0 + 28), (cx + 11, y1 - 6)], fill=GOLD)


def art_quake(pen, box):
    x0, y0, x1, y1 = box
    mid = (y0 + y1) // 2
    pen.line([(x0 + 6, y1 - 8), (x1 - 6, y1 - 8)], fill=SOFT, width=3)
    zig = [(x0 + 8, mid), (x0 + 34, mid - 16), (x0 + 52, mid + 14),
           (x0 + 74, mid - 22), (x0 + 96, mid + 10), (x0 + 118, mid - 8),
           (x1 - 10, mid)]
    pen.line(zig, fill=RED, width=4, joint="curve")
    pen.line([(x0 + 60, y1 - 8), (x0 + 74, y1 - 26)], fill=INK, width=3)
    pen.line([(x1 - 40, y1 - 8), (x1 - 30, y1 - 22)], fill=INK, width=3)


def art_block(pen, box):
    x0, y0, x1, y1 = box
    bx, by = x0 + 30, y0 + 10
    bw, bh = 62, 40
    pen.rectangle([bx, by, bx + bw, by + bh], fill=NAVY)
    for row in range(3):
        for col in range(3):
            wx = bx + 8 + col * 19
            wy = by + 6 + row * 12
            pen.rectangle([wx, wy, wx + 11, wy + 8],
                          fill=GOLD if (row + col) % 2 else PAPER)
    dx, dy = x1 - 36, y0 + 16
    pen.rectangle([dx - 9, dy - 4, dx + 9, dy + 4], fill=INK)
    for sx in (-1, 1):
        for sy in (-1, 1):
            rx, ry = dx + sx * 20, dy + sy * 10
            pen.line([(dx + sx * 9, dy), (rx, ry)], fill=INK, width=2)
            pen.ellipse([rx - 8, ry - 2, rx + 8, ry + 2], fill=INK)
    pen.line([(dx, dy + 4), (dx, dy + 12)], fill=INK, width=2)


def art_ship(pen, box):
    x0, y0, x1, y1 = box
    pen.polygon([(x0 + 14, y1 - 22), (x1 - 14, y1 - 22), (x1 - 34, y1 - 4),
                 (x0 + 30, y1 - 4)], fill=NAVY)
    for i, col in enumerate((RED, GOLD, SEA)):
        cx = x0 + 34 + i * 34
        pen.rectangle([cx, y1 - 46, cx + 28, y1 - 22], fill=col,
                      outline=INK, width=1)
    pen.line([(x0 + 60, y1 - 46), (x0 + 60, y1 - 62)], fill=INK, width=3)
    for ox, oy, rr in ((58, 14, 9), (76, 6, 12), (98, 2, 8)):
        pen.ellipse([x0 + ox - rr, y0 + oy - rr, x0 + ox + rr, y0 + oy + rr],
                    fill=(150, 150, 148))


def art_tanker(pen, box):
    x0, y0, x1, y1 = box
    pen.rounded_rectangle([x0 + 12, y1 - 30, x1 - 12, y1 - 10], radius=7,
                          fill=RED, outline=INK, width=2)
    for i in range(3):
        tx = x0 + 34 + i * 40
        pen.rounded_rectangle([tx, y1 - 52, tx + 32, y1 - 28], radius=6,
                              fill=PAPER, outline=INK, width=2)
    for wy in (y1 - 4, y1 + 2):
        pen.line([(x0 + 8, wy), (x1 - 8, wy)], fill=SEA, width=2)
    bx, by = x1 - 30, y1 - 58
    pen.polygon([(bx, by - 10), (bx + 5, by - 3), (bx + 12, by - 8),
                 (bx + 7, by), (bx + 12, by + 7), (bx + 4, by + 3),
                 (bx, by + 10), (bx - 4, by + 3), (bx - 12, by + 7),
                 (bx - 7, by), (bx - 12, by - 8), (bx - 5, by - 3)],
                fill=FLAME)


ARTISTS = {"globe": art_globe, "flame": art_flame, "quake": art_quake,
           "block": art_block, "ship": art_ship, "tanker": art_tanker}


# ---------------------------------------------------------------- page

def draw_masthead(pen, y):
    margin = 34
    right = 1024 - margin
    rule(pen, margin, right, y, weight=3)
    y += 12
    pen.text((margin, y), "No. 328", font=FACES.small, fill=INK)
    date = "MONDAY 23 NOVEMBER 2026"
    pen.text((right - pen.textlength(date, font=FACES.small), y), date,
             font=FACES.small, fill=INK)
    y += 30
    title = "THE WORLD TODAY"
    tw = pen.textlength(title, font=FACES.masthead)
    pen.text(((1024 - tw) / 2, y), title, font=FACES.masthead, fill=INK)
    y += 100
    rule(pen, margin, right, y, weight=4)
    return y + 12


def draw_lead(pen, y):
    margin = 34
    text_w = 636
    art_x = margin + text_w + 22
    art_w = 1024 - margin - art_x
    top = y
    pen.text((margin, y), LEAD_KICKER, font=FACES.kicker, fill=RED)
    y += 26
    y = para(pen, margin, y, text_w, LEAD_HEAD, FACES.headline, INK, 1.08)
    y += 6
    rule(pen, margin, margin + text_w, y, weight=1)
    y += 10
    y = para(pen, margin, y, text_w, LEAD_DECK, FACES.deck, INK, 1.3)
    y += 8
    y = para(pen, margin, y, text_w, LEAD_BODY, FACES.body, SOFT, 1.32)
    art_top = top + 4
    art_bottom = max(y, art_top + 250)
    pen.rectangle([art_x, art_top, art_x + art_w, art_bottom],
                  outline=INK, width=2)
    ARTISTS["globe"](pen, (art_x + 6, art_top + 6,
                           art_x + art_w - 6, art_bottom - 6))
    return art_bottom + 8


def draw_card(pen, box, card):
    x0, y0, x1, y1 = box
    pen.rectangle([x0, y0, x1, y1], outline=INK, width=1)
    ARTISTS[card["art"]](pen, (x0 + 8, y0 + 6, x1 - 8, y0 + 52))
    rule(pen, x0 + 10, x1 - 10, y0 + 56, weight=1, fill=SOFT)
    ty = y0 + 62
    pen.text((x0 + 10, ty), card["kick"], font=FACES.small, fill=RED)
    ty += 20
    ty = para(pen, x0 + 10, ty, x1 - x0 - 20, card["head"],
              FACES.card_head, INK, 1.12)
    ty += 4
    para(pen, x0 + 10, ty, x1 - x0 - 20, card["body"], FACES.card_body,
         SOFT, 1.15)


def draw_quote(pen, box):
    x0, y0, x1, y1 = box
    pen.rectangle([x0, y0, x1, y1], fill=NAVY)
    pen.text((x0 + 12, y0 + 8), "\u201c", font=face(SERIF_BOLD, 54),
             fill=GOLD)
    ty = y0 + 62
    ty = para(pen, x0 + 14, ty, x1 - x0 - 28, QUOTE_TEXT, FACES.quote,
              PAPER, 1.2)
    ty += 10
    for line in QUOTE_ATTR.split("\n"):
        pen.text((x0 + 14, ty), line, font=FACES.small, fill=(210, 214, 222))
        ty += 19


def draw_grid(pen, y):
    margin = 34
    gap = 12
    col_w = (1024 - 2 * margin - 2 * gap) // 3
    row_h = 186
    cells = []
    for row in range(2):
        for col in range(3):
            x0 = margin + col * (col_w + gap)
            cells.append((x0, y + row * (row_h + gap),
                          x0 + col_w, y + row * (row_h + gap) + row_h))
    for box, card in zip(cells[:5], CARDS):
        draw_card(pen, box, card)
    draw_quote(pen, cells[5])
    return y + 2 * row_h + gap


def draw_briefs(pen, y):
    margin = 34
    label = "IN BRIEF"
    pen.text((margin, y), label, font=FACES.small, fill=INK)
    rule(pen, margin + pen.textlength(label, font=FACES.small) + 12,
         1024 - margin, y + 8, weight=1)
    y += 24
    col_w = (1024 - 2 * margin - 24) // 2
    for i, (tag, text) in enumerate(BRIEFS):
        col = i // 3
        row = i % 3
        x = margin + col * (col_w + 24)
        by = y + row * 28
        pen.rectangle([x, by + 3, x + 8, by + 11], fill=RED)
        head_w = pen.textlength(tag + "  ", font=FACES.brief_bold)
        pen.text((x + 15, by), tag, font=FACES.brief_bold, fill=INK)
        lines = wrap_text(pen, text, FACES.brief, col_w - 15 - head_w)
        pen.text((x + 15 + head_w, by), lines[0] if lines else "",
                 font=FACES.brief, fill=SOFT)
        if len(lines) > 1:
            pen.text((x + 15, by + 14), lines[1], font=FACES.brief,
                     fill=SOFT)
    return y + 3 * 28 + 4


def draw_footer(pen, y):
    margin = 34
    rule(pen, margin, 1024 - margin, y, weight=3)
    y += 8
    line = "THE WORLD TODAY  ·  No. 328  ·  Monday 23 November 2026"
    tw = pen.textlength(line, font=FACES.tag)
    pen.text(((1024 - tw) / 2, y), line, font=FACES.tag, fill=SOFT)
    return y + 22


def compose():
    img = Image.new("RGB", CANVAS, PAPER)
    pen = ImageDraw.Draw(img)
    y = 20
    y = draw_masthead(pen, y)
    y = draw_lead(pen, y)
    y += 10
    y = draw_grid(pen, y)
    y += 8
    y = draw_briefs(pen, y)
    y += 4
    draw_footer(pen, y)
    return img


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(here, "news_image.png")
    compose().save(out, format="PNG")
    digest = hashlib.sha256(open(out, "rb").read()).hexdigest()
    size = os.path.getsize(out)
    print(f"wrote {out} ({size} bytes)")
    print(f"sha256 {digest}")


if __name__ == "__main__":
    main()
