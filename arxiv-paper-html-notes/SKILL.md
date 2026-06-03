---
name: arxiv-paper-html-notes
description: Generate Chinese static HTML paper notes, single-paper reading pages, or multi-paper review webpages from one or more arXiv links. Use when the user asks to turn arXiv papers into HTML notes, paper analysis pages, literature review webpages, meeting/group presentation pages, or a page similar to an existing arXiv-based paper note.
---

# arXiv Paper HTML Notes

## Goal

Create an offline, polished Chinese `index.html` paper note from one or more arXiv links. Default to the current research-note style: white background, deep blue/teal/wine accents, paper cards, paper figures, detailed method diagrams, validation details, comparison tables, and a bottom credit.

## Quick Workflow

1. Parse arXiv links from the user message.
2. Fetch metadata and PDFs with `scripts/extract_arxiv_metadata.py`.
3. Extract PDF text with `scripts/extract_pdf_text.py`.
4. Inspect official sources for code/model availability: arXiv comments, paper text, GitHub, Hugging Face, project pages. Mark uncertainty honestly.
5. Select or extract a method/overview figure from each PDF with `scripts/render_pdf_figures.py`; use a self-drawn CSS method diagram if no suitable figure is available.
6. Build `paper_notes.json` using the schema in `references/content_schema.md`.
7. Generate `index.html` with `scripts/assemble_html.py` and the template in `assets/html-template/`.
8. Validate HTML structure, links, image paths, desktop/mobile layout, and content traceability.

## Output Rules

- Write Chinese content unless the user explicitly requests another language.
- Produce a self-contained static `index.html` plus `assets/` images.
- For 1 paper, create a single-paper deep note and omit empty comparison sections.
- For 2-6 papers, create a review page with hero navigation, overview metrics, per-paper cards, comparison table, synthesis, references, and credits.
- Include a clickable hero card for each paper that jumps to the matching paper section.
- Keep paper card body single-column: information table first, then figure, method visual, data/method/validation details, and summary.
- Add the bottom credit:
  - `AI-assisted paper analysis · Generated with <generator_name>,`
  - `📝 Paper Analysis & Curation by CocoSun`
  - Use `generator_name` in `paper_notes.json` when the calling tool should be named explicitly, for example `Codex`, `Claude Code`, or `GitHub Copilot`.

## Content Requirements

Read `references/content_schema.md` before drafting `paper_notes.json`.

Each paper must include:

- Basic information: title, arXiv link/version, short name, domain/disease/organ, one-sentence positioning.
- Open-source status: confirmed official links or `未检索到明确公开代码/权重`.
- Dataset details: cohorts, slide/patch/ROI counts, modalities, centers, internal/external/prospective split when available.
- Methodology: backbone, pretraining objective, adaptation strategy, aggregation/task heads, clinical thresholds or deployment logic.
- Downstream validation: task categories, metrics, baselines, external/prospective/reader/clinical utility evidence.
- Figure: paper figure or self-drawn algorithm schematic, with a clear caption.
- Paper summary: research positioning, technical contribution, validation system, clinical meaning.

## Visual Requirements

Read `references/visual_style.md` before creating or modifying HTML/CSS.

Core layout:

- Hero: title, scope, clickable paper navigation cards.
- Overview metrics: paper count, organ/disease count, task/validation highlights.
- Paper stack: one card per paper, each with consistent structure.
- Comparison table: only when there are at least 2 papers.
- Synthesis: trends, common paradigm, strengths, limitations, future direction.
- References: arXiv and confirmed official project/model/code links.

## Verification Checklist

Read `references/paper_analysis_checklist.md` before final delivery.

Minimum checks:

- Metadata matches arXiv title/version/PDF.
- Numbers and claims are traceable to the paper or official project/model pages.
- Unconfirmed code/model release is not described as open source.
- All local image paths exist.
- All external links are clickable.
- HTML tags close correctly.
- Desktop and mobile layouts do not have obvious overflow or left/right mismatch.

## Useful Scripts

- Use a Python 3.10+ environment. Install `pypdf` for text extraction and `pypdfium2` for rendering PDF figures when those packages are not already available.
- `python scripts/extract_arxiv_metadata.py <arxiv-url-or-id>... --out metadata.json`
- `python scripts/extract_pdf_text.py <pdf-or-url> --out paper.txt` requires `pypdf`.
- `python scripts/render_pdf_figures.py <pdf> --page 6 --out assets/paper_figure.png [--crop x0,y0,x1,y1] [--scale 3]` requires `pypdfium2`.
- `python scripts/assemble_html.py paper_notes.json --out index.html --asset-dir assets`

Scripts are helpers, not substitutes for reading and reasoning. Always inspect the extracted text and correct summaries manually.
