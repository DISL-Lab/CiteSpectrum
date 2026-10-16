# CiteSpectrum citation data

**77,015 citation events · 550 paper entries · 150 original paper sources.** The survey collection includes four AI-involved writing conditions for each model and one shared Human baseline. The method collection adds 50 AI and 50 Human papers.

| Collection | Papers | Citation events |
|:---|---:|---:|
| LLM-Only surveys | 100 | 16,798 |
| RAG surveys | 100 | 13,792 |
| Outline-Guided surveys | 100 | 10,468 |
| Text-Guided surveys | 100 | 15,206 |
| Shared Human-Authored surveys | 50 | 12,856 |
| AI method papers | 50 | 2,412 |
| Human method papers | 50 | 5,483 |
| **Total** | **550** | **77,015** |

## Find a paper

- [All 550 complete paper titles](CATALOG.md)
- [Original authors, paper titles, sources, and source terms](SOURCES.md)
- [Manifest](manifest.json) · [Flat CSV index](papers.csv)
- [0-hop surveys](0hop/) · [Method papers](methods/)

Each paper has a stable three-digit directory ID, a README identifying the full focal-paper title, `citations.jsonl`, and `references.jsonl`. Titles are kept in metadata rather than used as long directory names. Paths in the manifest are relative to `data/`.

## Format

Files are UTF-8 JSON Lines: each nonempty line is one JSON object. Read them line by line without loading an entire collection into memory.

```python
import json
from pathlib import Path

root = Path("data")
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
paper = next(p for p in manifest["papers"] if p["paper_id"] == "survey:gpt54:rag:001")
with (root / paper["path"]).open(encoding="utf-8") as f:
    for line in f:
        citation = json.loads(line)
        print(citation["sentence"], citation["title"])
```

### Citation fields

| Field | Meaning |
|:---|:---|
| `sentence` | Actual source passage containing the citation; OCR paragraphs can contain more than one sentence. |
| `marker_text` | Actual citation marker in that passage. |
| `refNo` | Identifier in this paper's companion `references.jsonl`. |
| `title` | Title of the **cited work**, or `null` when its identity/title is unresolved. |
| `source_reference_id` | Reference identity in this paper's reconstructed source catalog. |
| `reference_status` | Whether the cited work's identity/title was resolved in the source. |
| `reference_namespace` | Source numbering system: global, subsection-local, original Human, or method bibliography. |
| `marker_refNo` | Original number in a numeric citation marker, where applicable. |
| `marker_author_year` | Author/year parsed from a source marker, where applicable. |

The **focal paper's title** is the manifest's `title` and the heading of its README. A citation record's `title` identifies the reference it cites. These two titles serve different purposes.

`refNo` can differ from the printed number in `marker_text`: it resolves collisions between subsection-local, global, and retained original-paper numbers. Preserve the actual marker when comparing against the source. Multiple references in one marker produce multiple citation events; repeated passage text alone is not a duplicate event.

Companion references contain `refNo`, `title`, `source_reference_id`, `reference_status`, and `citation_cnt`, with source metadata where available. Method `authors` values are OCR-derived surname tokens used in matching, rather than a verified complete author list. Original focal-paper author attribution is in `sources.json` and each paper's README.

### Identity review statuses

| Status | Citation events | Meaning |
|:---|---:|:---|
| `resolved_in_source` | 75,940 | The work's identity/title was resolved in the citing source's bibliography. |
| `undefined_reference_in_source` | 937 | The source uses a number that its available reference lists do not define. |
| `unresolved_author_year_in_source` | 97 | No source bibliography entry could be uniquely linked to that author/year. |
| `ambiguous_author_year_in_source` | 24 | Several source entries match that author/year. |
| `source_title_quality_review` | 16 | Source title text needs review. |
| `source_title_missing` | 1 | The source entry omits the title. |

Unresolved titles are not guessed. Use `reference_status == "resolved_in_source"` when an analysis requires a resolved target. This status establishes source-bibliography identity; model-authored fabricated or inappropriate citations remain observations of the model's output.

## Pairing and indexing

The same survey `source_id` (`001`–`050`) refers to the same topic across all four conditions and both models. The shared Human baseline is stored once. Method IDs belong to their own AI/Human collections and do not pair with survey topic IDs.

| Manifest field | Meaning |
|:---|:---|
| `paper_id` | Unique corpus/model/condition/entry identifier. |
| `corpus`, `setting`, `condition`, `model` | Collection and writing condition; `model` is `null` for the Human baseline and method entries. |
| `source_id`, `stable_source_id` | Local entry ID; `stable_source_id` identifies paired survey topics. |
| `title` | Full focal-paper title. |
| `source_key` | Identifier in `sources.json` for original source attribution. |
| `source_title`, `source_authors`, `source_url`, `source_doi` | Original source attribution. |
| `source_license`, `source_license_url`, `text_license`, `annotation_license` | Licenses/source terms for the distinct materials. |
| `citation_count`, `resolved_count`, `unresolved_or_review_count` | Event counts for this paper. |
| `path`, `references_path` | Citation and reference paths relative to `data/`. |
| `sha256`, `references_sha256` | SHA-256 checksums of those files. |

See [examples/load_data.py](../examples/load_data.py) for streamed loading and paired-topic selection.

## Validation and release snapshot

The reviewed extraction checks body positions, actual marker strings, matching reference IDs/titles, and duplicate occurrence/target pairs. The audit covered 400 generated surveys, 2,255 focal Method MD OCR files, 67 original Method PDFs, and 16,342 reference OCR JSONs. The earlier restored Human baseline contributes 12,856 verified events.

The manuscript used the original extraction snapshot. Citation counts changed during repair; manuscript results have not been recomputed. Method titles follow original proceedings/source metadata where available, with extraction-version title changes recorded separately.

- [Audit summary](audit/summary.json)
- [Unresolved event index](audit/unresolved_citations.csv)
- [Primary-document metadata repairs](audit/primary_metadata_repairs.csv)
- [Method PDF title comparisons](audit/method_pdf_title_checks.csv)
- [Focal-paper title updates](audit/focal_title_updates.csv)
- [Data file checksums](file_hashes.json)

Run `python scripts/validate_data.py` from the repository root to validate the distributed files. No complete source PDFs or OCR documents are bundled.

## License and attribution

See [data licenses](LICENSE.md) and [original source attribution](SOURCES.md).

## Migration

The reviewed release uses `citations.jsonl` in place of the earlier `citations.json` arrays, adds companion reference catalogs, and consolidates indexing in `data/manifest.json`. Existing survey directory IDs and model/condition paths are retained. Method data lives under `data/methods/`.
