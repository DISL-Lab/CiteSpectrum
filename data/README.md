# CiteSpectrum: 0-hop survey data

The dataset pairs scientific surveys across five levels of AI involvement. This release contains the focal survey text at **hop 0**, organized by model and writing condition.

## Contents

| Model folder | Generator |
|:---|:---|
| [`0hop/gpt54/`](0hop/gpt54) | GPT-5.4 |
| [`0hop/qwen80b/`](0hop/qwen80b) | Qwen3-Next-80B-A3B-Instruct |

Each model folder contains `llm-only`, `rag`, `outline-guided`, `text-guided`, and `human-authored`, with **50 surveys per condition**.

There are **500 physical files and 450 unique surveys**: 400 AI-involved surveys, plus 50 human-authored surveys copied under both model folders. The human-authored copies are byte-identical; count them once when pooling models.

The 50 source topics span 14 domains: Psychology, Computer Science, Biology, Medicine, Chemistry, Engineering, Geography, Materials Science, Physics, Economics, Sociology, Mathematics, History, and Business.

## File format

Every paper directory holds one `survey_content.json` with this schema:

```json
{
  "title": "Survey title",
  "subsections": [
    {
      "section_title": "Section heading",
      "subsection_title": "Subsection heading",
      "content": "Survey prose with in-text citation markers."
    }
  ]
}
```

Subsections appear in document order. Citation markers are part of the `content` string. The hop-0 records contain the focal survey text; reference-paper files and citation-analysis annotations are separate study artifacts.

## Pairing surveys

The three-digit prefix in each paper directory is a **stable source ID**, from `001` to `050`. The same ID refers to the same source topic across all model–condition combinations. Generated titles can differ between conditions, so use `stable_source_id` to join records.

[`0hop/manifest.json`](0hop/manifest.json) indexes all 500 files. Each row in `surveys` provides:

| Field | Meaning |
|:---|:---|
| `model` | `gpt54` or `qwen80b` |
| `condition` | One of the five writing conditions |
| `stable_source_id` | Integer from 1 to 50, shared across model–condition pairs |
| `title` | Title stored in the corresponding survey |
| `path` | File path relative to `data/0hop/` |
| `sha256` | SHA-256 checksum of the survey JSON |

For example, load both models' RAG versions of source topic 1:

```python
import json
from pathlib import Path

root = Path("data/0hop")
manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
paired = {
    row["model"]: json.loads((root / row["path"]).read_text(encoding="utf-8"))
    for row in manifest["surveys"]
    if row["stable_source_id"] == 1 and row["condition"] == "rag"
}
```

## Relation to the paper

The full CiteSpectrum study analyzes **550 papers and 78,016 citation events**. Its survey subset has **450 unique papers and 73,586 citation events**; its method subset has 100 papers and 4,430 citation events. This release distributes the survey subset's text at hop 0.

See Section 3 and Appendix C of the paper for the study design, corpus construction, and statistics.
