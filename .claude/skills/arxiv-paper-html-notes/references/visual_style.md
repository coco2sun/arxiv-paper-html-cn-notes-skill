# Visual Style

Match the static research-note style used by CocoSun's pathology foundation model notes.

## Palette and typography

- Background: light gray page shell with white content canvas.
- Accents: deep blue `#163b66`, teal `#0f766e`, wine `#8f2444`, small amber/green accents.
- Font stack: system Chinese UI fonts, no external font dependency.
- Avoid one-note palettes, decorative blobs, and marketing hero layouts.

## Page structure

1. Hero section
   - Eyebrow in English.
   - Large Chinese title.
   - 2-3 sentence Chinese summary.
   - Clickable paper navigation cards linking to each paper card.
2. Overview metrics
   - Paper count, organ/disease count, approximate task count, validation highlight.
3. Paper cards
   - Single-column body, never left table vs right long content.
   - Info table first.
   - Paper figure next.
   - Detailed algorithm schematic next.
   - Data/method/validation detail panels.
   - Paper summary card.
4. Cross-paper comparison
   - Use a horizontally scrollable table for 2+ papers.
5. Synthesis and references.
6. Bottom credit.

## Paper card rules

- Add stable section IDs: `paper-{id}`.
- The hero card for each paper must link to the matching section ID.
- Use `scroll-behavior: smooth` and `scroll-margin-top` for good navigation.
- Keep figures `object-fit: contain`; use max-height around 720-780 px on desktop and 420 px on mobile.
- Keep method diagrams in CSS cards, not giant paragraphs.

## Method diagram pattern

Use this structure:

```html
<div class="method-visual">
  <div class="visual-title">模型详细算法示意<span>short technical subtitle</span></div>
  <div class="method-lane">
    <div class="lane-title">1. Data Curation</div>
    <div class="method-box"><b>Label</b><small>Detail</small></div>
  </div>
  <div class="formula-strip">
    <div class="formula">Key formula or data flow</div>
  </div>
</div>
```

## Responsive rules

- At desktop width, paper body remains single-column.
- Detail panels use `repeat(auto-fit, minmax(280px, 1fr))`.
- Tables must be wrapped in an overflow-x container.
- On mobile, hero cards, metrics, summaries, references, and formulas become single-column.
