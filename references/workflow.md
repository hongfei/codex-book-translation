# Visual-First Workflow

## Core Position

- Original book pages are the visual authority; extracted text or Markdown is only an editable working draft.
- The core intermediate format is not a single Markdown file, but `page-map.json`, `book-map.json`, optional `segments.jsonl`, and semantic XHTML.
- Render page images before extracting text; translation, layout, and validation must all refer back to page images.
- The final EPUB should be reflowable text whenever possible; use cropped images only for figures, tables, formulas, illustrations, and complex layout regions.

## Recommended Steps

1. Save the original book in `original/`, recording edition, page count, author, and copyright-page information.
2. Use `scripts/render_pages.py` to generate `pages/page-images/`.
3. Create `structure/page-map.json` to record page structure and special elements.
4. Create `structure/book-map.json` to record whole-book logical order, page ranges, chapter files, figures, and notes.
5. Extract text into `src/extracted-text/` while preserving page anchors; generate `structure/segments.jsonl` if alignment is needed.
6. Edit translation drafts in `src/target-draft-md/`, or maintain `src/target-xhtml/` directly.
7. Use `src/target-xhtml/` as the semantic input for EPUB construction.
8. Reflow figures and tables when reliable; otherwise crop them from page images.
9. Prefer placing notes close to the annotated paragraph; if notes must be moved to the back, add bidirectional links.
10. After building the EPUB, perform human final review against the page images.

## Intermediate Format Responsibilities

- `page-map.json`: Page-level visual structure; answers "what is on this page?"
- `book-map.json`: Whole-book logical structure; answers "in what order does content enter the book?"
- `segments.jsonl`: Source/translation alignment; answers "where did this translated passage come from?"
- Markdown: Human-editable draft; answers "does the translation read naturally?"
- XHTML: Publishing-semantic source; answers "how should the EPUB render correctly?"

## When to Use Whole-Page Screenshots

Use whole-page screenshots only when the user explicitly requests them, or when the target is a facsimile/fixed-layout book. Ordinary EPUBs should not be built from whole-page screenshots.
