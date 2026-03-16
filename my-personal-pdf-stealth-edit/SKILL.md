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

Check with: `python3 SKILL_DIR/scripts/check_deps.py`

## The Complete Workflow

Follow these 5 phases in strict order. Each phase has a script in `scripts/`.

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
python3 SKILL_DIR/scripts/forensic_verify.py <modified.pdf> <original.pdf>
```

Runs the 13-point check:

| # | Check | Detects |
|---|-------|---------|
| 1 | Binary marker bytes (offsets 10-13) | qpdf/pikepdf/tool signatures |
| 2 | PDF version header | Version mismatch |
| 3 | `%%EOF` count | Incremental updates |
| 4 | `xref` section count | Incremental updates |
| 5 | Tool string scan in binary | Any tool name in file |
| 6 | `/ID` field in trailer | Added by qpdf/pikepdf |
| 7 | Trailer padding | Residue from removed fields |
| 8 | Object count | Extra objects from overlays |
| 9 | Producer/Author metadata | Tool signatures in metadata |
| 10 | `BT`/`ET` text block count | Overlay text blocks |
| 11 | White fill operators (`1 1 1 rg`) | White rectangle overlays |
| 12 | File size delta (< 1%) | Excessive additions |
| 13 | `CreationDate == ModDate` | Post-creation modification sign |

All 13 must pass. Additionally: decompress and compare content streams, verify operator sequences are identical, confirm no new streams added.

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
