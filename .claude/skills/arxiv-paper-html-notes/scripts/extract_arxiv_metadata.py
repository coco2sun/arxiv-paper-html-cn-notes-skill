#!/usr/bin/env python3
"""Fetch basic arXiv metadata for one or more arXiv IDs/URLs."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path


ARXIV_API = "https://export.arxiv.org/api/query"


def normalize_id(value: str) -> str:
    value = value.strip()
    match = re.search(r"arxiv\.org/(?:abs|pdf)/([^?#\s]+)", value)
    if match:
        value = match.group(1)
    value = value.removesuffix(".pdf")
    if not re.match(r"^[a-z-]+/\d{7}|\d{4}\.\d{4,5}(v\d+)?$", value):
        # Keep unknown but still query; arXiv will return no entry if invalid.
        return value
    return value


def fetch(ids: list[str]) -> list[dict]:
    query = urllib.parse.urlencode({"id_list": ",".join(ids)})
    request = urllib.request.Request(
        f"{ARXIV_API}?{query}",
        headers={"User-Agent": "arxiv-paper-html-notes/1.0 (local Codex skill; contact: local-user)"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            xml_text = response.read()
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"arXiv API request failed with HTTP {exc.code}. Retry later or fetch metadata from the arXiv abs page manually.") from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"arXiv API request failed: {exc.reason}") from exc
    root = ET.fromstring(xml_text)
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    records = []
    for entry in root.findall("atom:entry", ns):
        arxiv_id_url = entry.findtext("atom:id", default="", namespaces=ns)
        arxiv_id = arxiv_id_url.rstrip("/").split("/")[-1]
        links = []
        pdf_url = ""
        for link in entry.findall("atom:link", ns):
            attrs = link.attrib
            href = attrs.get("href", "")
            links.append({"title": attrs.get("title", ""), "rel": attrs.get("rel", ""), "href": href})
            if attrs.get("title") == "pdf" or attrs.get("type") == "application/pdf":
                pdf_url = href
        records.append(
            {
                "id": arxiv_id,
                "version": re.search(r"(v\d+)$", arxiv_id).group(1) if re.search(r"(v\d+)$", arxiv_id) else "",
                "title": " ".join(entry.findtext("atom:title", default="", namespaces=ns).split()),
                "summary": " ".join(entry.findtext("atom:summary", default="", namespaces=ns).split()),
                "authors": [a.findtext("atom:name", default="", namespaces=ns) for a in entry.findall("atom:author", ns)],
                "published": entry.findtext("atom:published", default="", namespaces=ns),
                "updated": entry.findtext("atom:updated", default="", namespaces=ns),
                "primary_category": (entry.find("arxiv:primary_category", ns).attrib.get("term", "") if entry.find("arxiv:primary_category", ns) is not None else ""),
                "categories": [c.attrib.get("term", "") for c in entry.findall("atom:category", ns)],
                "abs_url": arxiv_id_url,
                "pdf_url": pdf_url or f"https://arxiv.org/pdf/{arxiv_id}",
                "links": links,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("items", nargs="+", help="arXiv IDs or arXiv abs/pdf URLs")
    parser.add_argument("--out", default="-", help="Output JSON path, or '-' for stdout")
    args = parser.parse_args()

    records = fetch([normalize_id(item) for item in args.items])
    data = {"papers": records}
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if args.out == "-":
        print(text)
    else:
        Path(args.out).write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
