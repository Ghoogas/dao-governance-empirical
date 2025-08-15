import time, requests, pandas as pd
from pathlib import Path
REF = "data/reference/dao_ids.csv"
OUT = Path("data/processed/defillama_treasury.csv")
BASE = "https://api.llama.fi"
def _get(path):
    for i in range(5):
        r = requests.get(BASE+path, timeout=60)
        if r.status_code == 404: return None
        try:
            r.raise_for_status(); return r.json()
        except Exception:
            time.sleep(0.5*(i+1))
    raise RuntimeError(f"DefiLlama failed: {path}")
def fetch_row(slug):
    if not slug or pd.isna(slug): return {}
    try:
        data = _get(f"/treasury/{slug}")
    except Exception:
        return {}
    if not data: return {}
    # shape can vary; normalize a few common fields
    latest = None
    for k in ("chainTvls","treasury","totalUsd"):
        if k in data:
            latest = data[k] if not isinstance(data[k], dict) else data[k].get("value")
            break
    return {"defillama_slug": slug, "treasuryUSD": latest}
def main():
    ref = pd.read_csv(REF)
    rows=[]
    for _,r in ref.iterrows():
        d = fetch_row(r.get("defillama_slug"))
        rows.append({"id": r["id"], **d})
        time.sleep(0.2)
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("wrote", OUT, "rows", len(rows))
if __name__=="__main__": main()
