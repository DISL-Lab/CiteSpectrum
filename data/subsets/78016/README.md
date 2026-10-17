# 78,016-event subset

**78,016 events · 550 papers.** This is a reproducible subset of the 80,627-event corrected release.

All generated Survey 1–4 events and all Method AI/Human events are retained. Human surveys contribute 13,719 events, allocated proportionally across all 50 papers by largest remainder. Rows within each paper are selected by a fixed SHA-256 ranking and returned in original source order. No citation text or reference identity changes during selection.

The event count equals the manuscript's reported total. This selection is distinct from the manuscript's original extraction snapshot, and the manuscript results have not been recomputed.

- [Exact selection and input checksums](selection.json)
- [Download the standalone subset](https://github.com/DISL-Lab/CiteSpectrum/releases/download/data-2026-10-17/CiteSpectrum-78016-20261017.zip)

The selection file references the full release instead of duplicating its JSONL files.

```python
from examples.load_data import papers, iter_citations

count = sum(1 for paper in papers(subset="78016") for _ in iter_citations(paper))
assert count == 78016
```

To create standalone per-paper citation and reference files:

```bash
python scripts/export_subset.py --subset 78016 --output ../CiteSpectrum-78016
python ../CiteSpectrum-78016/scripts/validate_data.py
```

To reproduce the selection file itself, run `python scripts/create_subset_selection.py` on the full release. Source-file and manifest checksums prevent applying a selection to a different extraction version.
