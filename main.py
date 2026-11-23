"""Ship the finished 23 November front page to the grading sandbox.

render.py (Pillow) paints news_image.png in advance; this entry point
only carries those bytes across to /output/entry.png. It uses nothing
beyond the Python standard library, so it runs with no network and no
extra packages installed.
"""

from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "news_image.png"
TARGET = Path("/output") / "entry.png"


def ship():
    if not SOURCE.is_file():
        raise SystemExit(f"cannot find {SOURCE.name} beside this file")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(SOURCE.read_bytes())
    print(f"wrote {TARGET} ({TARGET.stat().st_size} bytes)")


if __name__ == "__main__":
    ship()
