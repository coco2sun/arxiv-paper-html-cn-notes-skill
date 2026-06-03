#!/usr/bin/env python3
"""Render paper_notes.json into a static HTML paper note."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = ROOT / "assets" / "html-template"


def esc(value: object) -> str:
    return html.escape("" if value is None else str(value), quote=True)


def slug(value: str) -> str:
    return "".join(ch if ch.isalnum() else "-" for ch in value.lower()).strip("-") or "paper"


def link_list(links: list[dict]) -> str:
    return "\n".join(
        f'<a href="{esc(link.get("url", ""))}" target="_blank" rel="noopener">{esc(link.get("label", "link"))}</a>'
        for link in links
        if link.get("url")
    )


def method_visual(paper: dict) -> str:
    lanes = []
    for step in paper.get("method_steps", []):
        boxes = "\n".join(
            f'<div class="method-box"><b>{esc(item.get("label", ""))}</b><small>{esc(item.get("detail", ""))}</small></div>'
            for item in step.get("items", [])
        )
        lanes.append(f'<div class="method-lane"><div class="lane-title">{esc(step.get("title", ""))}</div>{boxes}</div>')
    formulas = "".join(f'<div class="formula">{esc(f)}</div>' for f in paper.get("formulas", []))
    chips = "".join(f'<span class="mini-chip">{esc(c)}</span>' for c in paper.get("chips", []))
    return f"""
      <div class="method-visual">
        <div class="visual-title">{esc(paper.get("short_name", "Paper"))}详细算法示意<span>{esc(paper.get("method_subtitle", "method overview"))}</span></div>
        {''.join(lanes)}
        {f'<div class="formula-strip">{formulas}</div>' if formulas else ''}
        {f'<div class="mini-chip-grid">{chips}</div>' if chips else ''}
      </div>
    """


def detail_panel(title: str, icon: str, items: list[str]) -> str:
    bullets = "".join(f"<li>{esc(item)}</li>" for item in items)
    return f'<div class="note-panel"><h4 data-icon="{esc(icon)}">{esc(title)}</h4><ul>{bullets}</ul></div>'


def paper_card(paper: dict) -> str:
    pid = slug(paper.get("id") or paper.get("short_name", "paper"))
    links = link_list(paper.get("links", []))
    figure = ""
    if paper.get("figure_path"):
        figure = f"""
          <figure class="paper-figure">
            <img src="{esc(paper.get("figure_path"))}" alt="{esc(paper.get("short_name", "paper"))} figure">
            <figcaption>{esc(paper.get("figure_caption", ""))}</figcaption>
          </figure>
        """
    summary = paper.get("paper_summary", {})
    summary_items = "".join(
        f'<div class="summary-item"><b>{esc(item.get("label", ""))}</b><span>{esc(item.get("text", ""))}</span></div>'
        for item in summary.get("items", [])
    )
    details = paper.get("details", {})
    tags = "".join(f'<span class="tag">{esc(tag)}</span>' for tag in [paper.get("domain"), paper.get("version")] if tag)
    status = f'<span class="status">{esc(paper.get("opensource_status", ""))}</span>' if paper.get("opensource_status") else ""
    return f"""
      <article class="model-card" id="paper-{pid}">
        <div class="model-head">
          <div class="model-title">
            <h3>{esc(paper.get("short_name", ""))}</h3>
            <p class="paper-title">{esc(paper.get("title", ""))}</p>
            <div class="badge-row">{tags}{status}</div>
          </div>
          <div class="model-links">{links}</div>
        </div>
        <div class="model-body">
          <table class="info-table">
            <tr><th>基础信息</th><td>{esc(paper.get("positioning", ""))}</td></tr>
            <tr><th>数据集</th><td>{esc(paper.get("dataset_summary", ""))}</td></tr>
            <tr><th>方法学</th><td>{esc(paper.get("method_summary", ""))}</td></tr>
            <tr><th>开源</th><td>{esc(paper.get("opensource_status", ""))}</td></tr>
          </table>
          <div>
            {figure}
            {method_visual(paper)}
            <p class="method-detail"><b>方法要点：</b>{esc(paper.get("clinical_value", ""))}</p>
            <div class="deep-dive">
              {detail_panel("数据集细节", "DATA", details.get("data", []))}
              {detail_panel("方法学细节", "METH", details.get("method", []))}
              {detail_panel("验证结果细节", "VAL", details.get("validation", paper.get("validation_results", [])))}
            </div>
            <div class="paper-summary">
              <h4>{esc(paper.get("short_name", "Paper"))} 论文概括总结</h4>
              <p>{esc(summary.get("paragraph", ""))}</p>
              <div class="summary-grid">{summary_items}</div>
            </div>
          </div>
        </div>
      </article>
    """


def render(data: dict) -> str:
    papers = data.get("papers", [])
    hero_cards = "".join(
        f'<a class="organ-pill" href="#paper-{slug(p.get("id") or p.get("short_name", "paper"))}"><strong>{esc(p.get("short_name", ""))}</strong><span>{esc(p.get("domain", ""))}</span></a>'
        for p in papers
    )
    metrics = [
        (len(papers), "论文数量"),
        (len({p.get("domain", "") for p in papers if p.get("domain")}), "疾病/器官方向"),
        (sum(len(p.get("validation_results", [])) for p in papers), "验证要点"),
        ("HTML", "离线科研笔记"),
    ]
    metric_html = "".join(f'<div class="metric"><span class="value">{esc(v)}</span><span class="label">{esc(k)}</span></div>' for v, k in metrics)
    cards = "\n".join(paper_card(paper) for paper in papers)
    comparison = ""
    if len(papers) >= 2:
        rows = ""
        for p in papers:
            c = p.get("comparison", {})
            rows += f"<tr><td><b>{esc(p.get('short_name', ''))}</b></td><td>{esc(p.get('domain', ''))}</td><td>{esc(c.get('backbone', ''))}</td><td>{esc(c.get('pretraining_data', ''))}</td><td>{esc(c.get('task_scope', ''))}</td><td>{esc(c.get('clinical_validation', ''))}</td><td>{esc(c.get('open_source', p.get('opensource_status', '')))}</td></tr>"
        comparison = f"""
          <section class="band">
            <div class="section-head"><h2>横向对比</h2><p class="section-note">对比各论文的疾病/器官、基础模型、数据、任务和转化证据。</p></div>
            <div class="table-wrap"><table class="comparison"><thead><tr><th>模型</th><th>方向</th><th>Backbone</th><th>预训练数据</th><th>任务范围</th><th>临床验证</th><th>开源情况</th></tr></thead><tbody>{rows}</tbody></table></div>
          </section>
        """
    syn = data.get("synthesis", {})
    insight_items = syn.get("trends", []) or [syn.get("overview", "")]
    insights = "".join(f'<div class="insight"><h3>{esc(item.get("title", "综合分析") if isinstance(item, dict) else "综合分析")}</h3><p>{esc(item.get("text", "") if isinstance(item, dict) else item)}</p></div>' for item in insight_items if item)
    refs = "".join(f'<li>{esc(p.get("short_name", ""))}：{link_list(p.get("links", []))}</li>' for p in papers)
    content = f"""
      <header class="hero">
        <div class="hero-content">
          <p class="eyebrow">{esc(data.get("eyebrow", "arXiv Paper Notes"))}</p>
          <h1>{esc(data.get("page_title", "arXiv 论文笔记"))}</h1>
          <p>{esc(data.get("hero_summary", ""))}</p>
          <div class="hero-grid" aria-label="论文导航">{hero_cards}</div>
        </div>
      </header>
      <section class="band"><div class="section-head"><h2>整体图景</h2><p class="section-note">这些指标用于快速定位论文范围和验证强度。</p></div><div class="metric-grid">{metric_html}</div></section>
      <section><div class="section-head"><h2>逐篇论文笔记</h2><p class="section-note">每篇按统一结构整理基础信息、数据、方法、验证和总结。</p></div><div class="model-stack">{cards}</div></section>
      {comparison}
      <section><div class="section-head"><h2>综合分析</h2><p class="section-note">{esc(syn.get("overview", ""))}</p></div><div class="insight-grid">{insights}</div></section>
      <section class="band"><div class="section-head"><h2>参考链接</h2><p class="section-note">仅列出 arXiv 与已确认官方链接。</p></div><ul class="refs">{refs}</ul><p class="footnote">整理日期：{esc(data.get("analysis_date", ""))}。若论文作者后续公开代码、权重或更新版本，建议同步更新。</p></section>
      <footer class="site-credit"><div>AI-assisted paper analysis · Generated with <strong>{esc(data.get("generator_name", "AI assistant"))}</strong>,</div><div>📝 Paper Analysis &amp; Curation by <strong>{esc(data.get("credit_name", "CocoSun"))}</strong></div></footer>
    """
    template = (TEMPLATE_DIR / "index.template.html").read_text(encoding="utf-8")
    style = (TEMPLATE_DIR / "style.css").read_text(encoding="utf-8")
    return template.replace("{{PAGE_TITLE}}", esc(data.get("page_title", "arXiv 论文笔记"))).replace("{{STYLE}}", style).replace("{{CONTENT}}", content)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", help="paper_notes.json path")
    parser.add_argument("--out", default="index.html", help="Output HTML path")
    parser.add_argument("--asset-dir", default="assets", help="Reserved for compatibility; assets are referenced from JSON")
    args = parser.parse_args()
    data = json.loads(Path(args.json_path).read_text(encoding="utf-8"))
    Path(args.out).write_text(render(data), encoding="utf-8")
    print(f"saved {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
