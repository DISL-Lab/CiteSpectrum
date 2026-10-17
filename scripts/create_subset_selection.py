"""Select 78,016 events while retaining all generated surveys and methods."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TARGET = 78016
SEED = "CiteSpectrum-2026-10-17-78016-v1"


def main():
    manifest_path = DATA / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    papers = manifest["papers"]
    human = [p for p in papers if p["setting"] == 5]
    fixed = sum(p["citation_count"] for p in papers if p["setting"] != 5)
    human_target = TARGET - fixed
    human_total = sum(p["citation_count"] for p in human)
    if not 0 < human_target <= human_total:
        raise ValueError("The full release cannot supply this subset with complete non-Human collections.")
    quotas = {p["paper_id"]: p["citation_count"] * human_target // human_total for p in human}
    remainder = human_target - sum(quotas.values())
    ranked = sorted(human, key=lambda p: (-(p["citation_count"] * human_target % human_total), p["paper_id"]))
    for p in ranked[:remainder]:
        quotas[p["paper_id"]] += 1
    selected = []
    for paper in papers:
        count = paper["citation_count"]
        rows = "all"
        if paper["setting"] == 5:
            count = quotas[paper["paper_id"]]
            if count < 1:
                raise ValueError("A paper would be omitted from the subset.")
            def rank(number):
                key = "\0".join([SEED, paper["paper_id"], paper["sha256"], str(number)])
                return hashlib.sha256(key.encode("utf-8")).digest()
            rows = sorted(sorted(range(1, paper["citation_count"] + 1), key=rank)[:count])
        selected.append({"paper_id": paper["paper_id"], "path": paper["path"],
                         "full_file_sha256": paper["sha256"], "citation_count": count, "rows": rows})
    assert sum(p["citation_count"] for p in selected) == TARGET
    selection = {
        "format_version": 1, "subset_id": "78016", "citation_events": TARGET,
        "full_citation_events": manifest["summary"]["citation_events"],
        "full_manifest_sha256": hashlib.sha256(manifest_path.read_bytes()).hexdigest(),
        "seed": SEED, "human_target": human_target, "complete_settings": [1, 2, 3, 4, 6, 7],
        "policy": "Retain every generated survey and method event. Allocate Human survey quotas proportionally by largest remainder, then select rows by SHA-256 rank with a fixed seed. Preserve source order within each paper.",
        "manuscript_snapshot": False, "papers": selected,
    }
    destination = DATA / "subsets" / "78016" / "selection.json"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(selection, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"citation_events": TARGET, "papers": len(papers),
                      "complete_non_human_events": fixed, "selected_human_events": human_target}, indent=2))


if __name__ == "__main__":
    main()
