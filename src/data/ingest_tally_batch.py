import os
import pandas as pd
from pathlib import Path

# uses the helper you just merged
from .ingest_tally import fetch_org  # noqa: F401

SLUGS_FILE = Path("data/reference/dao_slugs.txt")
OUT_DIR = Path("data/processed/tally")

def read_slugs(path: Path) -> list[str]:
    if not path.exists():
        raise FileNotFoundError(f"Slug file not found: {path}")
    slugs = []
    for line in path.read_text().splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        slugs.append(s)
    return slugs

def main(limit_per_org: int = 1000):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    slugs = read_slugs(SLUGS_FILE)

    summary_rows = []

    for slug in slugs:
        print(f"[tally] fetching proposals for '{slug}' …")
        try:
            records = fetch_org(slug, limit=limit_per_org)  # returns list of dicts
        except Exception as e:
            print(f"  ! error for {slug}: {type(e).__name__}: {e}")
            continue

        if not records:
            print(f"  · no proposals returned for {slug}")
            summary_rows.append({"slug": slug, "proposals": 0})
            continue

        df = pd.json_normalize(records)
        # write per-slug proposals file
        out_csv = OUT_DIR / f"{slug}_proposals.csv"
        df.to_csv(out_csv, index=False)
        print(f"  · wrote {len(df)} rows -> {out_csv}")

        # quick summary: total proposals (you can extend with states, etc.)
        summary_rows.append({"slug": slug, "proposals": len(df)})

    # write summary file
    if summary_rows:
        summary = pd.DataFrame(summary_rows).sort_values("slug")
        summary_csv = OUT_DIR / "tally_summary_proposal_counts.csv"
        summary.to_csv(summary_csv, index=False)
        print(f"[tally] summary -> {summary_csv}")
    else:
        print("[tally] nothing to summarize")

if __name__ == "__main__":
    main()
