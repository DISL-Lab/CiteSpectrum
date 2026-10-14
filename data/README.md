# CiteSpectrum: citation-event data

This release contains **73,586 citation events from 450 unique surveys**, paired across five levels of AI involvement and two model families. Each paper is decomposed into citation records and stored as a JSON array in `citations.json`.

## Contents

| Writing condition | GPT-5.4 events | Qwen3-Next-80B events |
|:---|---:|---:|
| LLM-Only | 10,527 | 5,728 |
| RAG | 10,519 | 3,277 |
| Outline-Guided | 7,059 | 3,350 |
| Text-Guided | 8,520 | 7,462 |
| **AI-involved subtotal** | **36,625** | **19,817** |

Each AI condition contains **50 papers per model**, for 400 AI-involved papers and 56,442 citation events. The **50 shared Human-Authored papers contain 17,144 events**, bringing the total to **450 papers and 73,586 events**. The shared baseline is stored once; use it for both models.

| Folder | Contents |
|:---|:---|
| [`0hop/gpt54/`](0hop/gpt54) | GPT-5.4: `llm-only`, `rag`, `outline-guided`, `text-guided` |
| [`0hop/qwen80b/`](0hop/qwen80b) | Qwen3-Next-80B-A3B-Instruct: the same four AI conditions |
| [`0hop/human-authored/`](0hop/human-authored) | Shared human baseline |
| [`0hop/manifest.json`](0hop/manifest.json) | Index, event counts, paper metadata, and SHA-256 checksums |

The 50 source topics span 14 domains: Psychology, Computer Science, Biology, Medicine, Chemistry, Engineering, Geography, Materials Science, Physics, Economics, Sociology, Mathematics, History, and Business.

## File format

Each `citations.json` is a UTF-8 JSON array. For example, the first record in [`0hop/gpt54/rag/001/citations.json`](0hop/gpt54/rag/001/citations.json) is:

```json
[
  {
    "sentence": "Work on the social phenotype in autism emphasizes that atypicality must be specified at multiple levels—from observable social behavior to underlying cognitive operations and neural mechanisms—because similar behavioral outcomes may arise from different developmental pathways ref [29].",
    "refNo": 29,
    "title": "A Review of Cardiac Autonomic Measures: Considerations for Examination of Physiological Response in Children with Autism Spectrum Disorder",
    "marker_text": "[29]"
  }
]
```

| Field | Meaning |
|:---|:---|
| `sentence` | Sentence containing the citation |
| `refNo` | Reference identifier local to the focal paper |
| `title` | Extracted title of the cited work |
| `marker_text` | Citation marker captured during extraction; optional |
| `extraction_method` | Extraction method recorded by the source pipeline; optional |

The export preserves the source citation records and their order, including optional fields. A sentence citing several works can appear in several records. Count array entries as citation events; keep repeated sentences when analyzing event-level behavior.

## Pairing papers

The paper-directory name is a three-digit **stable source ID**, from `001` to `050`. The same ID refers to the same source topic across all model–condition combinations. Generated titles can differ, so join papers using `stable_source_id`.

The manifest's `papers` array indexes all 450 citation files. Paths are relative to `data/0hop/`.

| Field | Meaning |
|:---|:---|
| `paper_id` | Unique identifier for the model, condition, and source topic |
| `model` | `gpt54` or `qwen80b`; `null` for the shared human baseline |
| `condition` | `llm-only`, `rag`, `outline-guided`, `text-guided`, or `human-authored` |
| `stable_source_id` | Integer from 1 to 50 |
| `source_title` | Title of the original survey defining the paired topic |
| `title` | Title of the focal paper |
| `citation_count` | Number of records in its citation array |
| `path` | Relative path to `citations.json` |
| `sha256` | SHA-256 checksum of the exported JSON file |

Load the same source topic across all five conditions for GPT-5.4:

```python
import json
from pathlib import Path

root = Path("data/0hop")
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
paired = {
    paper["condition"]: json.loads((root / paper["path"]).read_text(encoding="utf-8"))
    for paper in manifest["papers"]
    if paper["stable_source_id"] == 1 and paper["model"] in ("gpt54", None)
}
print(sorted(paired))
# ['human-authored', 'llm-only', 'outline-guided', 'rag', 'text-guided']

print(sum(paper["citation_count"] for paper in manifest["papers"]))
# 73586
```

## Relation to the paper

The full CiteSpectrum study analyzes **550 papers and 78,016 citation events**. This release contains the survey subset: **450 unique papers and 73,586 citation events**. The method subset comprises another 100 papers and 4,430 events.

See Section 3 and Appendix C of the paper for the study design, corpus construction, and statistics.
