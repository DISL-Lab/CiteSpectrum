"""Stream citation data and pair survey topics using the standard library."""
import json
import hashlib
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data"


@lru_cache(maxsize=4)
def subset_selection(subset):
    selection = json.loads((DATA / "subsets" / str(subset) / "selection.json").read_text(encoding="utf-8"))
    actual = hashlib.sha256((DATA / "manifest.json").read_bytes()).hexdigest()
    if selection["full_manifest_sha256"] != actual:
        raise ValueError("This subset selection belongs to a different full release.")
    return {p["paper_id"]: p for p in selection["papers"]}


def papers(subset=None):
    result = json.loads((DATA / "manifest.json").read_text(encoding="utf-8"))["papers"]
    if subset is None:
        return result
    selected = subset_selection(subset)
    output = []
    for paper in result:
        item = selected[paper["paper_id"]]
        resolved = paper["resolved_count"]
        if item["rows"] != "all":
            resolved = sum(row["reference_status"] == "resolved_in_source"
                           for row in iter_citations(paper, subset=subset))
        output.append({**paper, "full_citation_count": paper["citation_count"],
                       "citation_count": item["citation_count"], "resolved_count": resolved,
                       "unresolved_or_review_count": item["citation_count"] - resolved,
                       "subset_id": str(subset)})
    return output


def iter_citations(paper, *, resolved_only=False, subset=None):
    subset = subset or paper.get("subset_id")
    indices = None
    if subset is not None:
        rows = subset_selection(subset)[paper["paper_id"]]["rows"]
        if rows != "all":
            indices = set(rows)
    with (DATA / paper["path"]).open(encoding="utf-8") as file:
        for number, line in enumerate(file, 1):
            if indices is not None and number not in indices:
                continue
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
