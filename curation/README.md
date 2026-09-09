# HIPE local curation

This work addresses the upstream issue backlog in a v3.0 release generated from v2.1. It does not replace the original benchmark or claim improved NER
scores. Source inspected: commit `147f5bc` of the user's repository.

## Run

From this directory:

```sh
python3 -m unittest discover -s tests -v
python3 tools/curate.py --repo .. --output ../data/v3.0
```

The output directory must not exist. `corrections.json` guards each correction
with its document ID, line and complete original row. The tool audits all 66
HIPE task TSVs in v2.1; supplementary OCR correction tables are copied unchanged but not audited.
`audit.json` includes input hashes and before/after findings. It reports six
annotation layers separately, so counts are not unique entities. Masked file
variants are included and may duplicate findings.

## Issue status

The `issues/` folder mirrors all 10 upstream issues, including four closed ones,
with comments retrieved on 2026-09-09. Pull requests are excluded. Original
authors, URLs and timestamps are retained; credential query parameters are
redacted. Linked images and CSV attachments remain links. This is a local
archive, not newly created GitHub issues. Upstream issue states are unchanged.

| Issue | Local outcome |
| --- | --- |
| #14 | Restore 10-token Reinach person span using author PR #15. Preserve Savoie as nested `loc.adm.reg`; outer link is Q202790. |
| #16 | Correct four-token outer ORG/inner PER structure using author PR #17; set outer Q56322697 consistently. Preserve existing Vogler annotation policy. |
| #18 | Correct five `sieur` titles. Other comments (parentheses, missing outer entities, name components) remain for contextual adjudication. |
| #19 | Correct Victio to pers/pers.ind in race standings; retain OCR spelling and existing QID. |
| #20 | Reproduced at French train line 135787. Unresolved: changing I-org to I-loc, or excluding the adjective, needs a consistent literal/metonymic boundary decision. |
| #21 | Document-level training export avoids splitting at EndOfSentence. Model-specific windowing still needs implementation; never simply turn every continuation into B. |
| #2, #4, #9, #13 | Closed upstream; archived for provenance, not reopened or independently revalidated. |

The first audit reports 395 invalid BIO transitions and 1,642 continuations
across sentence markers. The 20 targeted row edits do not change these totals.
The derivative is therefore not yet a fully validated training release.

The correction manifest intentionally uses v2.1 paths and original row values as
provenance. Generated task filenames use v3.0. Primary-dataset metadata versions
and original_source fields retain their source values.

## NER work next

Use `prepare_documents.py INPUT OUTPUT.jsonl` for individual train/dev files.
It preserves full documents and fails on invalid coarse BIO labels, exposing
remaining annotation errors rather than converting them silently. It excludes
test files. The exporter is preparation code, not a trained model.

Establish the current historical-gliner baseline, then compare independently:
original versus curated training data, document context, and OCR augmentation.
Keep original test data fixed for benchmark comparability; report any separately
adjudicated test evaluation under a distinct name. Preserve corpus-specific tag
semantics and evaluate by dataset/language, using the official HIPE scorer.
Choose models, compute budget and overflow strategy before launching training.

Original dataset licenses and attribution continue to apply. No upstream files,
issues or GitHub repositories are modified by these tools.
