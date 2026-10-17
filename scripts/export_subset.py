"""Materialize a selected release, including matching references and checksums."""
import argparse
import collections
import csv
import hashlib
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def records(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_records(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path, rows):
    fields = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value
                             for key, value in row.items()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--subset", default="78016")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"Output already exists: {output}")
    selection_path = ROOT / "data" / "subsets" / args.subset / "selection.json"
    selection = load(selection_path)
    assert selection["full_manifest_sha256"] == digest(ROOT / "data" / "manifest.json")
    selected = {paper["paper_id"]: paper for paper in selection["papers"]}
    shutil.copytree(ROOT, output, ignore=shutil.ignore_patterns(".git", "__pycache__", "subsets"))
    data = output / "data"
    manifest = load(data / "manifest.json")
    before = json.loads(json.dumps(manifest))
    statuses = collections.Counter()
    settings = collections.defaultdict(collections.Counter)
    hashes = []
    unresolved = []
    line_maps = {}
    for paper in manifest["papers"]:
        item = selected[paper["paper_id"]]
        citation_path = data / paper["path"]
        reference_path = data / paper["references_path"]
        old_rows = records(citation_path)
        assert digest(citation_path) == item["full_file_sha256"]
        indices = list(range(1, len(old_rows) + 1)) if item["rows"] == "all" else item["rows"]
        rows = [old_rows[number - 1] for number in indices]
        line_maps[paper["path"]] = {old: new for new, old in enumerate(indices, 1)}
        counts = collections.Counter(row["source_reference_id"] for row in rows)
        refs = records(reference_path)
        for ref in refs:
            ref["citation_cnt"] = counts[ref["source_reference_id"]]
        save_records(citation_path, rows)
        save_records(reference_path, refs)
        local = collections.Counter(row["reference_status"] for row in rows)
        paper.update(citation_count=len(rows), resolved_count=local["resolved_in_source"],
                     unresolved_or_review_count=len(rows) - local["resolved_in_source"],
                     sha256=digest(citation_path), references_sha256=digest(reference_path))
        statuses.update(local)
        settings[str(paper["setting"])].update(papers=1, citations=len(rows),
            resolved=paper["resolved_count"], unresolved_or_review=paper["unresolved_or_review_count"])
        hashes.extend([{"path": paper["path"], "sha256": paper["sha256"]},
                       {"path": paper["references_path"], "sha256": paper["references_sha256"]}])
        for number, row in enumerate(rows, 1):
            if row["reference_status"] != "resolved_in_source":
                unresolved.append({"path": paper["path"], "line": number, "refNo": row["refNo"],
                    "source_reference_id": row["source_reference_id"], "status": row["reference_status"],
                    "marker_text": row["marker_text"]})
        readme = citation_path.parent / "README.md"
        text = readme.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^[\d,]+ citation events · [\d,]+ source-resolved · [\d,]+ unresolved / title review\.$",
            f'{len(rows):,} citation events · {paper["resolved_count"]:,} source-resolved · {paper["unresolved_or_review_count"]:,} unresolved / title review.', text)
        readme.write_text(text, encoding="utf-8")
    count = sum(p["citation_count"] for p in manifest["papers"])
    assert count == selection["citation_events"] == 78016
    summary = manifest["summary"]
    summary.update(citation_events=count, survey_citation_events=sum(p["citation_count"] for p in manifest["papers"] if p["setting"] <= 5),
        method_citation_events=sum(p["citation_count"] for p in manifest["papers"] if p["setting"] >= 6),
        resolved_events=statuses["resolved_in_source"], unresolved_or_review_events=count-statuses["resolved_in_source"],
        settings={key: dict(value) for key, value in settings.items()}, reference_statuses=dict(statuses),
        subset_id=args.subset, parent_citation_events=before["summary"]["citation_events"],
        subset_selection_sha256=digest(selection_path), manuscript_snapshot=False)
    summary["scope"] = "Deterministic 78,016-event subset of the corrected extraction release; all generated surveys and methods retained."
    save(data / "manifest.json", manifest)
    save(data / "file_hashes.json", hashes)
    write_csv(data / "papers.csv", [{**p, "source_authors": "; ".join(p["source_authors"])} for p in manifest["papers"]])
    write_csv(data / "audit" / "unresolved_citations.csv", unresolved)
    provenance_path = data / "audit" / "extraction_provenance.jsonl"
    if provenance_path.exists():
        proofs = []
        for proof in records(provenance_path):
            line_map = line_maps[proof["path"]]
            if proof["line"] in line_map:
                proofs.append({**proof, "full_release_line": proof["line"], "line": line_map[proof["line"]]})
        save_records(provenance_path, proofs)
    catalog_path = data / "CATALOG.md"
    catalog = catalog_path.read_text(encoding="utf-8")
    grouped = collections.defaultdict(list)
    for paper in manifest["papers"]:
        prior = next(p for p in before["papers"] if p["paper_id"] == paper["paper_id"])
        suffix = f']({Path(paper["path"]).parent.as_posix()}/) | '
        catalog = catalog.replace(suffix + f'{prior["citation_count"]:,} |', suffix + f'{paper["citation_count"]:,} |')
        grouped[Path(paper["path"]).parent.parent].append(paper)
    catalog_path.write_text(catalog, encoding="utf-8")
    for relative, papers in grouped.items():
        readme = data / relative / "README.md"
        text = readme.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^50 papers · [\d,]+ citation events\.$", f'50 papers · {sum(p["citation_count"] for p in papers):,} citation events.', text)
        for paper in papers:
            text = re.sub(rf'(?m)(\| {paper["source_id"]:03} \| .*? \| )[\d,]+( \|)$',
                          lambda match: match[1] + f'{paper["citation_count"]:,}' + match[2], text)
        readme.write_text(text, encoding="utf-8")
    replacements = {
        before["summary"]["citation_events"]: count,
        before["summary"]["survey_citation_events"]: summary["survey_citation_events"],
        before["summary"]["settings"]["5"]["citations"]: settings["5"]["citations"],
    }
    for relative in ["README.md", "data/README.md"]:
        path = output / relative
        text = path.read_text(encoding="utf-8")
        for old, new in replacements.items():
            text = text.replace(f"{old:,}", f"{new:,}").replace(f"{old:,}".replace(",", "%2C"), f"{new:,}".replace(",", "%2C"))
        for status, old in before["summary"]["reference_statuses"].items():
            text = re.sub(rf'(`{re.escape(status)}` \| )[\d,]+( \|)',
                lambda match: match[1] + f'{statuses[status]:,}' + match[2], text)
        versions = ("This standalone archive contains **78,016 events across 550 papers**. "
                    f'The parent corrected release contains **{before["summary"]["citation_events"]:,} events**. '
                    "See [the exact parent-file selection](data/subset_selection.json) and "
                    "[the full release](https://github.com/DISL-Lab/CiteSpectrum/releases/tag/data-2026-10-17).")
        if relative.startswith("data/"):
            versions = versions.replace("data/subset_selection.json", "subset_selection.json")
        text = re.sub(r"<!-- DATA_VERSIONS_START -->[\s\S]*?<!-- DATA_VERSIONS_END -->", versions, text)
        text = text.replace("data/subsets/78016/", "data/subset_selection.json").replace("subsets/78016/", "subset_selection.json")
        text = text.replace("    ├── subsets/78016/          # Reproducible selection; no duplicate raw data", "    ├── subset_selection.json  # Exact membership in the parent release")
        notice = "**This archive is the 78,016-event subset.** All generated survey and method events are retained; Human survey events are selected reproducibly from the corrected full release. This is a new subset, not the manuscript's original extraction snapshot.\n\n"
        path.write_text(notice + text, encoding="utf-8")
    shutil.copyfile(selection_path, data / "subset_selection.json")
    save(data / "audit" / "subset_export.json", {"subset_id": args.subset, "citation_events": count,
        "parent_citation_events": before["summary"]["citation_events"], "papers": len(manifest["papers"]),
        "selection_sha256": digest(selection_path)})
    print(json.dumps({"output": str(output), "citation_events": count, "papers": len(manifest["papers"]),
                      "reference_statuses": dict(statuses)}, indent=2))


if __name__ == "__main__":
    main()
