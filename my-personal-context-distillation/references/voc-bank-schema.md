# VoC Bank Schema

Use `docs/context-sources/voc-bank.csv` as the persistent evidence layer for customer research.

Prefer CSV over Markdown for this file.

Why:

- row-based evidence is easier to append, sort, filter, and deduplicate
- spreadsheet tools can open it directly
- scripts and agents can process it more reliably than a long Markdown table
- it preserves quote-level traceability without forcing `know-your-customer.md` to become bulky

If an older `voc-bank.csv` exists with a previous schema, migrate the header and backfill the new columns before appending new rows.

## Required Columns

- `entry_id`
- `captured_at`
- `source_type`
- `platform`
- `source_label`
- `source_url`
- `date_seen`
- `quote`
- `quote_language`
- `evidence_kind`
- `capture_method`

## Recommended Analytical Columns

- `segment`
- `journey_stage`
- `theme_tags`
- `friction_type`
- `risk_type`
- `intensity`
- `evidence_notes`

## Column Intent

- `entry_id`: stable unique id for the row
- `captured_at`: when this row was added to the bank
- `source_type`: review, forum, reddit, interview, survey, comment, faq, etc.
- `platform`: site or platform name
- `source_label`: short human-readable label for the source
- `source_url`: direct URL when available
- `date_seen`: publication date or access date
- `quote`: the raw quote or tight quote excerpt
- `quote_language`: language of the quote
- `evidence_kind`: what kind of proof the row contains
- `capture_method`: how the row was obtained

Analytical columns are useful, but they are not raw truth. Treat them as metadata.

## Controlled Values

### `evidence_kind`

Use one of:

- `direct_user_voice`
- `official_product_statement`
- `search_snippet`
- `third_party_summary`
- `founder_seed`

Interpretation:

- `direct_user_voice` is the strongest evidence for core KYC claims
- `official_product_statement` can support product facts or visible objections, but not inner customer truth by itself
- `search_snippet` is weak evidence and should usually trigger deeper fetching, not final synthesis
- `third_party_summary` is supporting context, not primary customer truth
- `founder_seed` is directional input only and should not be treated as proof

### `capture_method`

Use one of:

- `direct_fetch`
- `search_result_snippet`
- `user_supplied`
- `manual_import`

Interpretation:

- `direct_fetch` is preferred whenever possible
- `search_result_snippet` is lower-confidence and must be called out as such
- `user_supplied` is appropriate for transcripts, interviews, surveys, or manually supplied research
- `manual_import` is acceptable when the evidence was pasted from a known source and the source is preserved

## Writing Rules

- preserve the quote as directly as possible
- do not rewrite the quote into polished marketing language
- do not invent a source URL
- if the source is partial, say so in `evidence_notes`
- if the row comes from a search snippet rather than a fetched page, mark it with `evidence_kind=search_snippet` and `capture_method=search_result_snippet`
- if a row is founder guidance rather than market proof, mark it with `evidence_kind=founder_seed`
- if multiple quotes are nearly identical, keep enough examples to preserve signal, but do not spam duplicates
- if a quote supports multiple tags, prefer a compact delimiter format in the CSV cell

## KYC Synthesis Rules

Core KYC claims should be supported mainly by rows marked `direct_user_voice`.

This applies especially to:

- segments
- current situation
- trigger moments
- JTBD
- current substitutes
- pains
- desired outcomes
- objections
- decision criteria
- trust signals

Rows marked `official_product_statement`, `search_snippet`, `third_party_summary`, or `founder_seed` can still be useful, but they should not carry those claims alone.

If a claim is supported only by lower-confidence evidence, either:

- mark it as partial, or
- leave it in `Open Questions`

## Bank-To-KYC Consistency Rule

If `know-your-customer.md` mentions:

- number of quotes
- number of validated themes
- number of categories
- coverage claims such as `6/6 validated`

those numbers must be derived from the actual rows currently in `voc-bank.csv`.

Do not report synthetic counts from memory.
Do not claim a category is validated if the bank has no supporting rows for it.

## Relationship To `know-your-customer.md`

Build the bank first, then synthesize.

- `voc-bank.csv` keeps the evidence
- `know-your-customer.md` keeps the durable synthesized understanding

Do not treat the bank as a finished narrative document.
Do not treat the KYC file as a replacement for the bank.
