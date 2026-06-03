#!/usr/bin/env python3
"""Extract text from a local or remote PDF."""

from __future__ import annotations

import argparse
import tempfile
import urllib.request
from pathlib import Path

def materialize_pdf(source: str) -> Path:
    if source.startswith(("http://", "https://")):
        suffix = ".pdf"
        handle = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        handle.close()
        urllib.request.urlretrieve(source, handle.name)
        return Path(handle.name)
    return Path(source)


def extract_text(pdf_path: Path) -> str:
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise SystemExit("Missing pypdf. Use a Python environment with pypdf installed, or install pypdf before extracting PDF text.") from exc

    reader = PdfReader(str(pdf_path))
    chunks = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks.append(f"\n\n--- Page {index} ---\n{text}")
    return "".join(chunks).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", help="Local PDF path or PDF URL")
    parser.add_argument("--out", default="-", help="Output text path, or '-' for stdout")
    args = parser.parse_args()

    text = extract_text(materialize_pdf(args.pdf))
    if args.out == "-":
        print(text)
    else:
        Path(args.out).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
