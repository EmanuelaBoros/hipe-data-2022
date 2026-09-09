# HIPE data v3.0 — corrected derivative

Released in EmanuelaBoros/hipe-data-2022, based on upstream HIPE-2022 v2.1.
This is an independent corrected release, not an official HIPE organizers’ release.

## Changes

- #14: Restore the 10-token Théodore Reinach person span, retaining Savoie as a nested location.
- #16: Correct the four-token Haasenstein & Vogler outer organization / inner person annotation and use its organization QID consistently.
- #18: Change five occurrences of the honorific sieur from function to title.
- #19: Correct the cyclist Victio from organization to person, preserving OCR text and QID.

Total: 20 changed rows in three files (French and German HIPE2020 train; German NewsEye dev).
All 66 task TSVs are included with v3.0 filenames. Supplementary v2.1 files are copied unchanged.
Token text, document order, splits and original-source metadata are preserved.
Older releases are unchanged. Dataset licenses and attribution remain applicable.

## Limitations and reproducibility

This release does not resolve every annotation problem: #20 and parts of #18
remain open locally. The audit reports 395 invalid BIO transitions across six
annotation layers and 1,642 continuations across sentence markers, including
masked variants. These are findings, not counts of unique entities. #21 is
addressed by document-preserving preparation, without changing sentence markers.
No model improvement has yet been measured. The test annotations are unchanged.

See [curation tools](../../curation/README.md), [exact corrections](../../curation/corrections.json),
[archived issues](../../curation/issues/) and [audit](audit.json). Input hashes
refer to v2.1; audit keys refer to v3.0 files. To regenerate, run the curation
command with a new output directory; it refuses to overwrite an existing release.
