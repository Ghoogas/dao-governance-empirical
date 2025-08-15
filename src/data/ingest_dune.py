import os, time, requests, pandas as pd
from pathlib import Path
KEY=os.getenv("DUNE_API_KEY")
OUT=Path("data/processed/dune_metrics.csv")
REF="data/reference/dao_ids.csv"
BASE="https://api.dune.com/api/v1"
def run_query(query_id, params=None):
    if not KEY: return None
    h={"x-dune-api-key":KEY,"content-type":"application/json"}
    r = requests.post(f"{BASE}/query/{query_id}/execute", headers=h, json={"params":params or {}}, timeout=60)
    r.raise_for_status(); job=r.json()["execution_id"]
    # poll
    for _ in range(60):
        s = requests.get(f"{BASE}/execution/{job}/results", headers=h, timeout=60)
        if s.status_code==200: return s.json()["result"]["rows"]
        time.sleep(2)
    return None
def main():
    ref=pd.read_csv(REF)
    rows=[]
    for _,r in ref.iterrows():
        qid=r.get("dune_query_id")
        res=run_query(qid, params={"space": r["snapshot_space"]}) if not pd.isna(qid) else None
        val = res[0].get("voters_90d") if res else None
        rows.append({"id":r["id"], "voters_90d": val})
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("wrote", OUT)
if __name__=="__main__": main()
