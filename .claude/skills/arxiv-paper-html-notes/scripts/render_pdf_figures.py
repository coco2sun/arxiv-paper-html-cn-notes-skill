#!/usr/bin/env python3
"""Render a PDF page to PNG and optionally crop it."""

from __future__ import annotations

import argparse
from pathlib import Path


def parse_crop(value: str | None) -> tuple[int, int, int, int] | None:
    if not value:
        return None
    parts = [int(float(part.strip())) for part in value.split(",")]
    if len(parts) != 4:
        raise ValueError("--crop must be x0,y0,x1,y1")
    return tuple(parts)  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", help="Local PDF path")
    parser.add_argument("--page", type=int, required=True, help="1-based page number")
    parser.add_argument("--out", required=True, help="Output PNG path")
    parser.add_argument("--scale", type=float, default=3.0, help="Render scale")
    parser.add_argument("--crop", help="Optional crop box in rendered pixels: x0,y0,x1,y1")
    args = parser.parse_args()

    try:
        import pypdfium2 as pdfium
    except ModuleNotFoundError as exc:
        raise SystemExit("Missing pypdfium2. Install it in the active Python env or render/crop with another PDF tool.") from exc

    pdf = pdfium.PdfDocument(args.pdf)
    page_index = args.page - 1
    if page_index < 0 or page_index >= len(pdf):
        raise SystemExit(f"Page {args.page} out of range; PDF has {len(pdf)} pages")
    image = pdf[page_index].render(scale=args.scale).to_pil().convert("RGB")
    crop = parse_crop(args.crop)
    if crop:
        image = image.crop(crop)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out)
    print(f"saved {out} size={image.size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
