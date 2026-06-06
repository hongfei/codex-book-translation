# Codex Book Translation Skill

This repository contains the `publisher-grade-book-translation` Codex skill.

Use it to produce publisher-grade translated books from source books or PDFs: faithful translation, natural editorial polish, figure/table/note preservation, EPUB or ebook construction, and cross-checking against the original pages.

## Install

Copy or symlink the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
ln -s "$(pwd)/publisher-grade-book-translation" ~/.codex/skills/publisher-grade-book-translation
```

## System Dependencies

The skill itself is plain Markdown plus helper scripts. For the best end-to-end book translation workflow, install these tools:

Required for bundled scripts:
- Python 3
- `PyMuPDF` / `fitz`: renders PDF pages to PNG images.
- `Pillow` / `PIL`: crops regions, builds contact sheets, and validates images.

Recommended for publisher-grade book production:
- `epubcheck`: validates final EPUB packages.
- Java runtime: required by EPUBCheck.
- `pandoc`: converts between Markdown, HTML/XHTML, DOCX, and EPUB-adjacent formats.
- `poppler`: provides `pdftotext` and `pdfinfo` for PDF inspection and text extraction.
- `tesseract` plus `tesseract-lang`: OCR for scanned pages and multilingual source books.
- `imagemagick`: image inspection and conversion utilities.
- Calibre: provides `ebook-convert`, `ebook-polish`, `ebook-meta`, and other ebook utilities.
- `xmllint`, `zip`, and `unzip`: XML/XHTML and EPUB package checks.

On macOS with Homebrew:

```bash
brew install epubcheck pandoc poppler tesseract tesseract-lang imagemagick pymupdf pillow
brew install --cask calibre
```

Verify the important imports and commands:

```bash
python3 - <<'PY'
import fitz
import PIL
print("PyMuPDF", fitz.__version__)
print("Pillow", PIL.__version__)
PY

for cmd in epubcheck pandoc pdftotext pdfinfo tesseract magick ebook-convert xmllint zip unzip; do
  command -v "$cmd"
done
```

## Use

Invoke it explicitly in Codex:

```text
Use $publisher-grade-book-translation to translate this source book into a polished EPUB while preserving figures, notes, and structure.
```

The skill includes helper scripts for rendering PDF pages, cropping figures/tables, making crop contact sheets, and validating image assets.
