# Intermediate Format Principles

## Conclusion

Do not treat Markdown as the only intermediate format. Publisher-grade translation needs layered intermediate formats:

- Page images: visual authority.
- `page-map.json`: page-level structure.
- `book-map.json`: whole-book logical structure.
- `segments.jsonl`: optional source/translation alignment.
- Markdown: optional translation draft.
- XHTML: publishing-semantic source.

## Why Not Markdown Alone

Markdown is useful for body text, but it is not suitable for carrying:

- Precise note anchors
- Figure coordinates and crop information
- Multiple columns, sidebars, formulas, and complex tables
- Cross-page structure
- EPUB manifest/spine/nav semantics
- Verifiable resource references

## Recommended Practice

- Ordinary body text may be drafted in Markdown and then converted to XHTML.
- Figures, notes, quotations, and complex structures must be represented in JSON or XHTML.
- Final builds should rely mainly on `book-map.json` and `target-xhtml/`, not directly on Markdown.
- After converting Markdown to XHTML, perform manual spot checks so footnotes, lists, and heading levels are not mistransformed.
