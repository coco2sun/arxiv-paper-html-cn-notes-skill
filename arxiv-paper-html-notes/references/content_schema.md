# Content Schema

Use this schema for `paper_notes.json`. Keep the structure stable so `assemble_html.py` can render it.

## Top level

```json
{
  "page_title": "论文综述标题",
  "eyebrow": "Disease / Organ-Specific Pathology Foundation Models",
  "hero_summary": "2-3 句中文总述",
  "analysis_date": "YYYY-MM-DD",
  "generator_name": "Codex / Claude Code / GitHub Copilot / AI assistant",
  "credit_name": "CocoSun",
  "papers": [],
  "synthesis": {
    "overview": "总体研究情况",
    "trends": [],
    "strengths": [],
    "limitations": [],
    "future_directions": []
  }
}
```

## Paper object

Required fields:

```json
{
  "id": "stable-lowercase-id",
  "short_name": "PulmoFoundation",
  "title": "Full paper title",
  "arxiv_url": "https://arxiv.org/abs/...",
  "pdf_url": "https://arxiv.org/pdf/...",
  "version": "v1",
  "domain": "肺病理",
  "positioning": "一句话研究定位",
  "opensource_status": "已确认 Hugging Face gated 模型 / 未检索到明确公开代码/权重",
  "links": [
    {"label": "arXiv", "url": "..."}
  ],
  "figure_path": "assets/paper_overview.png",
  "figure_caption": "Paper Figure 1: ...",
  "dataset_summary": "短摘要",
  "method_summary": "短摘要",
  "method_steps": [
    {
      "title": "1. Data Curation",
      "items": [
        {"label": "40,000 WSIs", "detail": "具体说明"}
      ]
    }
  ],
  "details": {
    "data": [],
    "method": [],
    "validation": []
  },
  "validation_results": [],
  "clinical_value": "临床意义",
  "paper_summary": {
    "paragraph": "概括段",
    "items": [
      {"label": "研究定位", "text": "..."},
      {"label": "技术贡献", "text": "..."},
      {"label": "验证体系", "text": "..."},
      {"label": "临床意义", "text": "..."}
    ]
  },
  "comparison": {
    "backbone": "Virchow2 / ViT-L/16",
    "pretraining_data": "数据规模",
    "task_scope": "任务范围",
    "clinical_validation": "验证强度",
    "open_source": "开源情况"
  }
}
```

## Content defaults

- `id`: lowercase, hyphenated, no spaces.
- `generator_name`: optional; use the calling tool name when attribution matters. Defaults to `AI assistant` in the renderer.
- `figure_path`: use a local path under `assets/`; if no figure is available, leave empty and render a CSS method schematic only.
- `details.data`, `details.method`, `details.validation`: 3-8 bullet strings each.
- `method_steps`: 3-6 stages; each stage should have 2-5 items.
- `comparison`: required only for multi-paper pages.

## Single-paper behavior

For one paper, still use the same `papers[0]` schema. Omit cross-paper comparison and write synthesis as "这篇工作的研究定位与启示".
