"""Read-only validation of local paper archives and Markdown file links."""

import csv
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from pypdf import PdfReader


def main():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "literature/archive-manifest.json").read_text(encoding="utf-8-sig"))
    with (root / "literature/index.csv").open(encoding="utf-8-sig", newline="") as source:
        rows = {row["arxiv_id"]: row for row in csv.DictReader(source)}
    failures = []
    papers = []
    for record in manifest["papers"]:
        path = root / record["local_pdf"]
        if not path.is_file():
            failures.append(f"Missing PDF: {record['local_pdf']}")
            continue
        data = path.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        pages = len(PdfReader(path).pages)
        for condition, label in [
            (data.startswith(b"%PDF-"), "header"),
            (len(data) == record["bytes"], "size"),
            (digest == record["sha256"], "sha256"),
            (pages == record["page_count"], "page count"),
        ]:
            if not condition:
                failures.append(f"{record['alias']}: {label} mismatch")
        row = rows.get(record["arxiv_id"], {})
        for key in ("version", "title", "local_pdf", "sha256", "bytes", "page_count", "retrieved_at"):
            if str(row.get(key, "")) != str(record.get(key, "")):
                failures.append(f"{record['alias']}: CSV/manifest {key} mismatch")
        papers.append({"alias": record["alias"], "version": record["version"], "pages": pages, "bytes": len(data)})
    links_checked = 0
    # Only inline Markdown links with local file targets; online URL/anchor checks are separate.
    for source in root.rglob("*.md"):
        for match in re.finditer(r"\[[^\]]*\]\(([^\n)]+)\)", source.read_text(encoding="utf-8-sig")):
            target = match.group(1).strip().strip("<>")
            is_windows_path = bool(re.match(r"^[A-Za-z]:[/\\]", target))
            if target.startswith("#") or (urlsplit(target).scheme and not is_windows_path):
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            links_checked += 1
            if not (source.parent / target).exists():
                failures.append(f"Broken local link in {source.relative_to(root)}: {target}")
    report = {"pdf_count": len(papers), "papers": papers, "local_links_checked": links_checked, "failures": failures}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
