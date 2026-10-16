"""Stream citation data and pair survey topics using the standard library."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


def papers():
    return json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))["papers"]


def iter_citations(paper, *, resolved_only=False):
    with (DATA / paper["path"]).open(encoding="utf-8") as file:
        for line in file:
            record = json.loads(line)
            if not resolved_only or record["reference_status"] == "resolved_in_source":
                yield record


def paired_surveys(source_id, model="gpt54"):
    return {
        paper["condition"]: paper
        for paper in papers()
        if paper["corpus"] == "survey"
        and paper["source_id"] == source_id
        and paper["model"] in (model, None)
    }


if __name__ == "__main__":
    pair = paired_surveys(1)
    paper = pair["rag"]
    sample = next(iter_citations(paper, resolved_only=True))
    print(paper["title"])
    print(sample["marker_text"], "→", sample["title"])
    print("Paired conditions:", ", ".join(sorted(pair)))
