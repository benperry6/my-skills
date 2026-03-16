---
name: my-personal-pdf-stealth-edit
description: "[My Personal Skill] Use when the user wants to modify, alter, or edit text content (dates, names, numbers, amounts) inside an existing PDF while keeping the modification completely undetectable — even under forensic binary analysis. Triggers on: 'stealth edit PDF,' 'change date on PDF,' 'modify PDF invisibly,' 'edit ticket/receipt/invoice PDF,' or when user uploads a PDF and asks to change specific text values and implies it should look authentic or unmodified."
---

# PDF Stealth Edit

Modify any text content inside an existing PDF so that the result is indistinguishable from a natively generated original — both visually and under forensic binary analysis.

## Overview

PDFs encode text as **glyph codes** specific to each embedded font, not as readable characters. A naive approach (overlay white rectangles + new text, or regenerate with a library) leaves obvious traces. The only way to produce a truly invisible edit is to work at the **content stream level**, replacing glyph codes in place, then cleaning up structural traces left by the tools.

## Tool Dependencies

Must be available before starting:
- `qpdf` (CLI) — `brew install qpdf`
- `pikepdf` (Python) — `pip install pikepdf`
- `pdfplumber` (Python) — `pip install pdfplumber`
- `pypdf` (Python) — `pip install pypdf`
- `pypdfium2` (Python) — `pip install pypdfium2` (for visual verification)
- `Pillow` (Python) — `pip install Pillow` (for visual verification)

Check with: `python3 SKILL_DIR/scripts/check_deps.py`

## The Complete Workflow

Follow these 6 phases in strict order. Each phase has a script in `scripts/`.

### Phase 1 — Analyze the PDF

```bash
python3 SKILL_DIR/scripts/analyze_pdf.py <input.pdf> [--output analysis.json]
```

Extracts:
- **Metadata**: Producer, Author, CreationDate, ModDate (the "fingerprint" to preserve)
- **Structural baseline**: `%%EOF` count, `xref` sections, object count, binary marker bytes (offsets 10-13), trailer format, `/ID` field presence
- **Font map**: for each font, its encoding and CMap (Unicode → glyph hex code mapping)
- **Text extraction**: full text per page with character positions
- **Content stream inventory**: stream count, sizes, compression method

### Phase 2 — Map the Replacements

Before touching any bytes, build a **replacement plan**:

1. Identify every occurrence of text to change (all pages — headers, tables, fine print, EMD sections)
2. For each occurrence, determine which font renders it
3. Using that font's CMap, convert old text → hex glyph sequence and new text → hex glyph sequence
4. Verify every character in new text exists in the font's CMap — if missing, see Edge Cases
5. Handle length differences (padding with spacing operators or adjusting positioning)

This is the critical thinking step — get it wrong and you corrupt the PDF or leave visible artifacts.

### Phase 3 — Modify Content Streams

```bash
python3 SKILL_DIR/scripts/modify_streams.py <input.pdf> <output.pdf> --replacements replacements.json [--metadata metadata.json]
```

The script:
1. Opens the PDF with `pikepdf`
2. For each page containing text to modify:
   - Extracts content stream (handles FlateDecode decompression)
   - Locates hex string patterns matching old glyph sequences (inside `TJ`/`Tj` operators)
   - Replaces old hex with new hex
   - Recompresses with same filter
3. Updates metadata fields (CreationDate, ModDate, etc.)
4. Saves result

**Key principle**: only glyph data bytes change. Stream structure — operators, fonts, positions — stays identical. Same number of `BT`/`ET` blocks, `Tf`, `Td`, `Tm`, `TJ` operators.

### Phase 4 — Forensic Cleanup

```bash
python3 SKILL_DIR/scripts/forensic_clean.py <input.pdf> <output.pdf> --original <original.pdf>
```

Pipeline:

#### Step 1: Flatten with qpdf
```bash
qpdf --qdf input.pdf intermediate.pdf
qpdf intermediate.pdf flattened.pdf
```
Two passes: `--qdf` decomposes objects, second pass rebuilds cleanly. Eliminates extra `%%EOF`, extra `xref` sections, orphaned objects.

#### Step 2: Patch binary marker (qpdf signature)
qpdf writes `bf f7 a2 fe` at offsets 10-13. Replace with original PDF's marker bytes.

#### Step 3: Remove `/ID` field from trailer
qpdf adds `/ID [<hash1><hash2>]`. If the original didn't have it (most Amadeus, SAP, Oracle generators don't), remove it.

#### Step 4: Rebuild trailer cleanly
Deleting `/ID` leaves whitespace padding (forensic red flag). Instead: truncate at `trailer` offset, write clean trailer matching original format with correct `startxref`.

#### Step 5: Metadata coherence
Ensure `CreationDate == ModDate` and format matches original convention exactly.

### Phase 5 — Forensic Verification

```bash
python3 SKILL_DIR/scripts/forensic_verify.py <modified.pdf> <original.pdf> --full --expected-changes changes.json --output-dir ./diffs
```

Use `--full` to run all three verification layers in one command. Or run individually: `--deep` for stream analysis, `--visual` for pixel comparison.

#### Layer 1: 13-point binary forensic check

| # | Check | Detects | Pass condition |
|---|-------|---------|----------------|
| 1 | Binary marker bytes (offsets 10-13) | qpdf/pikepdf/tool signatures | Identical to original |
| 2 | PDF version header | Version mismatch | Identical to original |
| 3 | `%%EOF` count | Incremental updates | Same count as original |
| 4 | `xref` section count | Incremental updates | Same count as original |
| 5 | Tool string scan in binary | Any tool name in file | No foreign signatures |
| 6 | `/ID` field in trailer | Added by qpdf/pikepdf | Same presence/absence as original |
| 7 | Trailer padding | Residue from removed fields | No suspicious whitespace (>10 spaces) |
| 8 | Object count | Extra objects from overlays | Same count as original |
| 9 | Producer/Author metadata | Tool signatures in metadata | Identical to original |
| 10 | `BT`/`ET` text block count | Overlay text blocks | Same count as original |
| 11 | White fill operators (`1 1 1 rg`) | White rectangle overlays | Same count as original |
| 12 | File size delta | Excessive additions | < 1% difference |
| 13 | `CreationDate == ModDate` | Post-creation modification | Must be equal |

All 13 must pass.

#### Layer 2: Deep stream analysis

Decompresses and compares content streams between original and modified:
- Operator sequences must be identical (BT, ET, Tf, Td, TJ, etc.)
- Stream count per page must match
- No new streams added
- Only hex glyph data bytes should differ

#### Layer 3: Visual pixel-by-pixel verification (Phase 6)

See Phase 6 below.

### Phase 6 — Visual Verification

```bash
python3 SKILL_DIR/scripts/visual_verify.py <modified.pdf> <original.pdf> --expected-changes changes.json --output-dir ./diffs
```

Renders both PDFs at 300 DPI and compares every pixel. The key principle: **visual differences must exist ONLY where modifications were requested — nowhere else.**

#### Expected changes JSON

Provide a file describing what was modified so the script can verify diffs match:

```json
{
    "changes": [
        {"old": "05Mar2026", "new": "12Mar2026", "description": "departure date flight 1"},
        {"old": "01Mar2026", "new": "11Mar2026", "description": "issue date"}
    ]
}
```

#### Visual verification checks

| # | Check | Pass condition |
|---|-------|----------------|
| V1 | Page count | Modified == Original |
| V2 | Image dimensions per page | Identical sizes |
| V3 | Identical pages (no expected changes) | 0 different pixels |
| V4 | Modified pages — expected region diffs | All diff pixels fall within bounding boxes of old text |
| V5 | Modified pages — unexpected diffs | < 0.1% pixels outside expected regions (WARN for QR codes), 0% for PASS |
| V6 | Total diff percentage | < 0.5% of total pixels across all pages |

#### Output images

When `--output-dir` is provided, the script saves:
- `diff_pageN_highlighted.png` — original with diff pixels colored: **green** = expected region, **orange** = unexpected
- `diff_pageN_sidebyside.png` — cropped side-by-side of diff areas (ORIGINAL | MODIFIED)

These images serve as visual proof that the edit is invisible to the human eye.

#### QR codes and embedded data

QR codes, barcodes, or other encoded data that contain modified values will produce diff pixels outside text regions. This is expected behavior and produces a WARN (not FAIL) if < 0.1% of page pixels. **Always verify manually** that QR code content matches the modified text by scanning it.

## Edge Cases

- **Character not in font CMap**: Check if another font in the document has it. If visually similar glyph exists, use it. Last resort: micro-overlay (detectable under deep analysis).
- **Different-length replacements**: Shorter → pad with zero-width or adjust kerning in `TJ` array. Longer → reduce spacing. If difference too large, may not be feasible.
- **Encrypted PDFs**: `qpdf --decrypt` first, do NOT re-encrypt (or re-encrypt with same params).
- **Scanned PDFs (image-based)**: This skill doesn't apply — need image editing instead.

## Critical Principles

1. **Never use overlays** — white rectangles + new text is the #1 detection method.
2. **Never trust a single tool** — every PDF tool leaves fingerprints. The cleanup pipeline scrubs them.
3. **Always verify against the original** — forensic check catches forgotten `/ID` fields, binary markers.
4. **Preserve everything unchanged** — object count, stream count, operator sequences, font/image data.
5. **Metadata tells a story** — CreationDate, ModDate, Producer, Author must form a coherent narrative.
6. **Diffs must match intent exactly** — visual verification must confirm that the ONLY pixels that changed are the characters you meant to change. Any diff outside the expected modification regions is a red flag.
7. **Always save the expected-changes JSON** — it serves as both input for verification and as an audit trail of what was modified. Create it during Phase 2 (replacement mapping) and feed it through Phase 6.
