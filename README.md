# Codex Book Translation Skill

This repository contains the `publisher-grade-book-translation` Codex skill.

Use it to produce publisher-grade translated books from source books or PDFs: faithful translation, natural editorial polish, figure/table/note preservation, EPUB or ebook construction, and cross-checking against the original pages.

## Install

Copy or symlink the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/publisher-grade-book-translation" ~/.codex/skills/publisher-grade-book-translation
```

## Use

Invoke it explicitly in Codex:

```text
Use $publisher-grade-book-translation to translate this source book into a polished EPUB while preserving figures, notes, and structure.
```

The skill includes helper scripts for rendering PDF pages, cropping figures/tables, making crop contact sheets, and validating image assets.
