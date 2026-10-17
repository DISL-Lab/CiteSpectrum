"""Validate all released citation/reference files, indexes, and checksums."""
import collections
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


def unique_object(pairs):
    row = {}
    for key, value in pairs:
        assert key not in row, ("Duplicate JSON key", key)
        row[key] = value
    return row


def read_json(text):
    return json.loads(
        text,
        object_pairs_hook=unique_object,
        parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)),
    )


def records(path):
    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, 1):
            assert line.strip(), (path, line_number, "Empty JSONL line")
            row = read_json(line)
            assert isinstance(row, dict), (path, line_number, "Expected an object")
            yield row


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = read_json((DATA / "manifest.json").read_text(encoding="utf-8"))
    papers = manifest["papers"]
    source_rows = read_json((DATA / "sources.json").read_text(encoding="utf-8"))["sources"]
    sources = {s["source_key"]: s for s in source_rows}
    assert len(sources) == len(source_rows) == 150
    assert len(papers) == len({p["paper_id"] for p in papers}) == 550
    assert len(list(DATA.rglob("citations.jsonl"))) == 550
    assert len(list(DATA.rglob("references.jsonl"))) == 550
    assert not list(DATA.rglob("citations.json")), "Legacy citation arrays remain"
    event_count = 0
    statuses = collections.Counter()
    expected_paths = set()
    catalog = (DATA / "CATALOG.md").read_text(encoding="utf-8")
    for paper in papers:
        source = sources[paper["source_key"]]
        assert paper["source_title"] == source["title"]
        assert paper["source_license"] == source["license"]
        assert paper["annotation_license"] == "CC-BY-4.0"
        citation_path = DATA / paper["path"]
        reference_path = DATA / paper["references_path"]
        assert citation_path.resolve().is_relative_to(DATA.resolve())
        assert reference_path.resolve().is_relative_to(DATA.resolve())
        assert digest(citation_path) == paper["sha256"], paper["path"]
        assert digest(reference_path) == paper["references_sha256"], paper["references_path"]
        expected_paths.update([paper["path"], paper["references_path"]])
        readme = citation_path.parent / "README.md"
        assert readme.exists() and source["url"] in readme.read_text(encoding="utf-8")
        assert str(citation_path.parent.relative_to(DATA)).replace("\\", "/") + "/)" in catalog
        refs = list(records(reference_path))
        by_number = {r["refNo"]: r for r in refs}
        by_identity = {r["source_reference_id"]: r for r in refs}
        assert len(by_number) == len(by_identity) == len(refs)
        counts = collections.Counter()
        local_statuses = collections.Counter()
        local_count = 0
        for row in records(citation_path):
            ref = by_number[row["refNo"]]
            for field in ["source_reference_id", "title", "reference_status"]:
                assert row[field] == ref[field], (paper["paper_id"], field)
            assert isinstance(row["sentence"], str) and row["sentence"].strip()
            assert row["marker_text"] in row["sentence"], (paper["paper_id"], row["marker_text"])
            if row["reference_status"] == "resolved_in_source":
                assert isinstance(row["title"], str) and row["title"].strip()
            else:
                assert row["title"] is None
            assert not any(k.startswith("_") or k in {"body_source", "source_path"} for k in row)
            local_statuses[row["reference_status"]] += 1
            counts[row["source_reference_id"]] += 1
            local_count += 1
        assert local_count == paper["citation_count"]
        assert local_statuses["resolved_in_source"] == paper["resolved_count"]
        assert local_count - paper["resolved_count"] == paper["unresolved_or_review_count"]
        for ref in refs:
            assert ref["citation_cnt"] == counts[ref["source_reference_id"]]
            assert not any(k.startswith("_") for k in ref)
        event_count += local_count
        statuses.update(local_statuses)
    hashes = read_json((DATA / "file_hashes.json").read_text(encoding="utf-8"))
    assert len(hashes) == len(expected_paths) == 1100
    assert {x["path"] for x in hashes} == expected_paths
    for item in hashes:
        assert digest(DATA / item["path"]) == item["sha256"]
    assert event_count == manifest["summary"]["citation_events"]
    assert statuses["resolved_in_source"] == manifest["summary"]["resolved_events"]
    with (DATA / "audit/unresolved_citations.csv").open(encoding="utf-8-sig") as file:
        unresolved = list(csv.DictReader(file))
    assert len(unresolved) == event_count - statuses["resolved_in_source"]
    assert len(unresolved) == manifest["summary"]["unresolved_or_review_events"]
    for model in ["gpt54", "qwen80b"]:
        for condition in ["llm-only", "rag", "outline-guided", "text-guided"]:
            selection = [p for p in papers if p["model"] == model and p["condition"] == condition]
            assert len(selection) == 50
            assert {p["source_id"] for p in selection} == set(range(1, 51))
    subset_counts = {}
    for selection_path in sorted((DATA / "subsets").glob("*/selection.json")):
        selection = read_json(selection_path.read_text(encoding="utf-8"))
        assert selection["full_manifest_sha256"] == digest(DATA / "manifest.json")
        indexed = {p["paper_id"]: p for p in papers}
        chosen = selection["papers"]
        assert len(chosen) == len({p["paper_id"] for p in chosen}) == len(papers)
        count = 0
        for item in chosen:
            paper = indexed[item["paper_id"]]
            assert item["path"] == paper["path"]
            assert item["full_file_sha256"] == paper["sha256"]
            rows = item["rows"]
            if rows == "all":
                assert item["citation_count"] == paper["citation_count"]
            else:
                assert paper["setting"] == 5, "Complete generated/method collections must be preserved"
                assert rows == sorted(set(rows))
                assert rows and rows[0] >= 1 and rows[-1] <= paper["citation_count"]
                assert len(rows) == item["citation_count"]
            if paper["setting"] != 5:
                assert rows == "all"
            count += item["citation_count"]
        assert count == selection["citation_events"] == 78016
        subset_counts[selection["subset_id"]] = count
    provenance_path = DATA / "audit" / "extraction_provenance.jsonl"
    if provenance_path.exists():
        citation_cache = {}
        seen = set()
        for proof in records(provenance_path):
            path = proof["path"]
            if path not in citation_cache:
                citation_cache[path] = list(records(DATA / path))
            row = citation_cache[path][proof["line"] - 1]
            assert row["source_reference_id"] == proof["source_reference_id"]
            assert (path, proof["line"]) not in seen
            seen.add((path, proof["line"]))
    print(json.dumps({
        "papers": len(papers), "sources": len(sources), "citation_events": event_count,
        "checksums_verified": len(hashes), "reference_statuses": dict(statuses),
        "subsets": subset_counts, "errors": 0,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
