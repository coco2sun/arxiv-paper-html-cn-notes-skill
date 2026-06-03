# Agent Instructions

This repository stores reusable AI-agent skills.

When a user asks for Chinese HTML notes, single-paper reading pages, multi-paper review pages, literature-review pages, or meeting/group presentation pages from arXiv papers, use:

- `arxiv-paper-html-notes/SKILL.md`

Follow the skill's progressive workflow:

1. Read `SKILL.md`.
2. Load only the needed files from `references/`.
3. Use scripts from `scripts/` when available.
4. Generate `paper_notes.json`.
5. Render `index.html`.
6. Verify content traceability, links, local assets, and desktop/mobile layout.

Set `generator_name` in `paper_notes.json` to the tool that produced the page, for example `Codex`, `Claude Code`, `GitHub Copilot`, or `AI assistant`.

