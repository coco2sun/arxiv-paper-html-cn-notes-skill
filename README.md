# sun-skills

This repository stores reusable AI-agent skills. The current skill is:

- `arxiv-paper-html-notes`: generates polished Chinese static HTML notes from one or more arXiv papers.

## What It Does

`arxiv-paper-html-notes` helps an AI agent produce:

- single-paper deep reading pages
- multi-paper review pages
- Chinese literature-review webpages
- meeting or group-presentation style paper analysis pages

The skill bundles:

- `SKILL.md`: workflow and output rules
- `references/`: content schema, visual style, and verification checklist
- `scripts/`: arXiv metadata, PDF text extraction, PDF figure rendering, and HTML assembly helpers
- `assets/html-template/`: static HTML/CSS template

## Example Output

Example generated page:

- [APOLLO: A Virtual Patient Foundation Model](https://coco2sun.github.io/medical-ai-paper-notes/notes/apollo-virtual-patient-foundation-model/)

## Tool Compatibility

| Tool | Directly usable from this repo? | Status | Notes |
| --- | --- | --- | --- |
| Codex | No, not from the repo root automatically | Supported after install | Copy `arxiv-paper-html-notes/` to `~/.codex/skills/`. |
| Claude Code | Yes, project-level version included | Supported | This repo includes `.claude/skills/arxiv-paper-html-notes/`. |
| GitHub Copilot | Not as a `SKILL.md` skill | Supported through instructions | This repo includes `.github/copilot-instructions.md` and `.github/instructions/arxiv-paper-html-notes.instructions.md`. |
| Generic agents | Partially | Supported through `AGENTS.md` | Agents that read `AGENTS.md` can find the canonical skill. |

## Versions in This Repo

- `arxiv-paper-html-notes/`: canonical, tool-neutral skill package.
- `.claude/skills/arxiv-paper-html-notes/`: Claude Code project-level skill copy.
- `.github/copilot-instructions.md`: repository-wide GitHub Copilot entrypoint.
- `.github/instructions/arxiv-paper-html-notes.instructions.md`: Copilot task-specific instruction file.
- `AGENTS.md`: generic agent entrypoint.

If you edit the canonical skill, sync the Claude Code copy:

```bash
rm -rf .claude/skills/arxiv-paper-html-notes
cp -R arxiv-paper-html-notes .claude/skills/
```

## Install

### Codex

Install as a personal Codex skill:

```bash
mkdir -p ~/.codex/skills
cp -R arxiv-paper-html-notes ~/.codex/skills/
```

Then ask Codex for something like:

```text
Use the arxiv-paper-html-notes skill to generate a Chinese HTML note for https://arxiv.org/abs/....
```

### Claude Code

Project-level use is already prepared:

```text
.claude/skills/arxiv-paper-html-notes/
```

For global use across projects:

```bash
mkdir -p ~/.claude/skills
cp -R arxiv-paper-html-notes ~/.claude/skills/
```

Then ask Claude Code:

```text
Use the arxiv-paper-html-notes skill to create a Chinese review page for these arXiv papers: ...
```

### GitHub Copilot

Copilot does not automatically load `SKILL.md` as a skill. Use the included repository instructions:

```text
.github/copilot-instructions.md
.github/instructions/arxiv-paper-html-notes.instructions.md
```

In a Copilot chat, ask:

```text
Use the arxiv-paper-html-notes workflow in this repo to generate a Chinese HTML paper note for ...
```

## Python Dependencies

The helper scripts use Python 3.10+.

Install optional packages when needed:

```bash
python -m pip install pypdf pypdfium2
```

Script usage:

```bash
python arxiv-paper-html-notes/scripts/extract_arxiv_metadata.py <arxiv-url-or-id> --out metadata.json
python arxiv-paper-html-notes/scripts/extract_pdf_text.py <pdf-or-url> --out paper.txt
python arxiv-paper-html-notes/scripts/render_pdf_figures.py <pdf> --page 6 --out assets/paper_figure.png
python arxiv-paper-html-notes/scripts/assemble_html.py paper_notes.json --out index.html --asset-dir assets
```

## Usage Tips

- Always verify paper titles, arXiv versions, dataset numbers, and evaluation metrics against the paper or official source.
- Mark code/model availability as unknown unless confirmed from arXiv comments, official project pages, GitHub, or Hugging Face.
- Use `generator_name` in `paper_notes.json` to match the calling tool, such as `Codex`, `Claude Code`, or `GitHub Copilot`.
- For one paper, produce a deep single-paper page and omit empty comparison sections.
- For two to six papers, include paper navigation, comparison, synthesis, references, and credits.
- If figure extraction is unreliable, use a self-drawn CSS method diagram and leave `figure_path` empty.

### Prompt Templates

Single-paper deep note:

```text
Use the arxiv-paper-html-notes skill to generate a Chinese static HTML deep reading note for:
https://arxiv.org/abs/....

Output to notes/<paper-slug>/index.html.
Include paper metadata, dataset details, method diagram, validation results, open-source status, and a concise Chinese summary.
```

Multi-paper review page:

```text
Use the arxiv-paper-html-notes skill to create a Chinese multi-paper review page for these arXiv papers:

1. https://arxiv.org/abs/....
2. https://arxiv.org/abs/....
3. https://arxiv.org/abs/....

Group them by research direction, compare backbone, data scale, downstream tasks, clinical validation, and open-source status.
Output to notes/<topic-slug>/index.html.
```

Meeting or group-presentation style page:

```text
Use the arxiv-paper-html-notes skill to prepare a Chinese reading-group HTML page for these papers:
<arXiv links>

Focus on motivation, method pipeline, why the validation is convincing or weak, limitations, and discussion questions.
```

### Multi-Paper Tips

- Use two to six papers per page. More than six usually becomes too dense; split by disease, organ, modality, year, or model family.
- Put all arXiv links in one request when you want a comparison table and shared synthesis.
- Tell the agent the comparison angle if you already know it, for example `pathology foundation models for lung cancer`, `virtual patient models`, or `radiology multimodal agents`.
- Ask the agent to normalize paper names into short labels, such as `APOLLO`, `Virchow2`, or `UNI`.
- Ask for a stable output folder, such as `notes/pathology-foundation-models/index.html`, so assets and links stay organized.
- For review pages, require a final synthesis section covering shared trends, strongest evidence, weak spots, and future directions.
- If papers are from different domains, ask the agent to explain why they are grouped together; otherwise the comparison table can become shallow.
- For fresh papers, ask the agent to re-check official sources before judging code/model availability.

### Output Quality Checklist

- `paper_notes.json` follows `references/content_schema.md`.
- Every local image referenced by `figure_path` exists under the output `assets/` folder.
- Each paper has at least one arXiv link and any confirmed project/code/model links.
- Dataset numbers, model names, and benchmark metrics are traceable to the paper text or official sources.
- The HTML opens locally and does not have obvious desktop or mobile overflow.
- The footer uses the right `generator_name` and keeps `Paper Analysis & Curation by CocoSun`.
