---
applyTo: "**"
---

# arXiv Paper HTML Notes

Use these instructions when the user asks GitHub Copilot to turn one or more arXiv links into Chinese static HTML paper notes, a single-paper reading page, a multi-paper review page, or a meeting/group presentation page.

## Canonical Skill Package

The reusable skill lives at:

- `arxiv-paper-html-notes/SKILL.md`

Load that file first. It describes the workflow, output rules, reference files, scripts, and verification checklist.

## Copilot-Specific Usage

- Treat `arxiv-paper-html-notes/` as the source of truth.
- Set `generator_name` in `paper_notes.json` to `GitHub Copilot` when the generated page should name the calling tool.
- Use the bundled scripts when the local environment allows running Python:
  - `scripts/extract_arxiv_metadata.py`
  - `scripts/extract_pdf_text.py`
  - `scripts/render_pdf_figures.py`
  - `scripts/assemble_html.py`
- If Python packages are missing, tell the user to install `pypdf` and `pypdfium2`, or continue with manually collected paper text and a CSS method schematic.
- Do not claim code, models, or weights are open source unless confirmed from official sources such as arXiv comments, project pages, GitHub, or Hugging Face.
- Before delivery, verify that `index.html` renders, local image paths exist, external links work, and numerical claims trace back to the paper or official pages.

