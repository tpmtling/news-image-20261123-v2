#!/usr/bin/env python3
"""Entry point for news-image-20261123.

Standard library only. Copies the pre-rendered front page
(news_image.png, shipped in this repository) to the grader's output
path as entry.png, then reports the copy's size and sha256 so the two
runs can be checked for identical bytes.
"""

import hashlib
import os
import shutil
import sys

IMAGE_NAME = "news_image.png"
ENTRY_NAME = "entry.png"


def locate_source():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, IMAGE_NAME)


def locate_output():
    base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    return os.path.join(base, ENTRY_NAME)


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    src = locate_source()
    dst = locate_output()
    if not os.path.isfile(src):
        print(f"missing source image: {src}", file=sys.stderr)
        return 1
    parent = os.path.dirname(dst)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(src, dst)
    print(f"copied {src} -> {dst}")
    print(f"size {os.path.getsize(dst)} bytes")
    print(f"sha256 {digest(dst)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
