import os, time, requests, pandas as pd
from pathlib import Path
API = "https://api.tally.xyz/query"
KEY = os.getenv("TALLY_API_KEY")
HDR = {"content-type":"application/json","Api-Key":KEY} if KEY else {}
OUT = Path("data/processed/tally_gov.csv")
REF = "data/reference/dao_ids.csv"
Q = """
query($org:String!, $first:Int!, $after:String) {
  organization(slug:$org) {
    proposals(first:$first, after:$after) {
      pageInfo { endCursor hasNextPage }
      nodes { id state votes counts { abstain for against } quorum }
    }
  }
}
"""
def fetch_org(slug):
    if not KEY or not slug or pd.isna(slug): return []
    out=[]; after=None
    while True:
        r = requests.post(API, headers=HDR, json={"query":Q,"variables":{"org":slug,"first":200,"after":after}}, timeout=60)
        if r.status_code==401: raise RuntimeError("Set TALLY_API_KEY")
        r.raise_for_status(); data=r.json()
        org = data.get("data",{}).get("organization")
        if not org: break
        page = org["proposals"]["nodes"]; out += page
        pi = org["proposals"]["pageInfo"]
        if not pi["hasNextPage"]: break
        after = pi["endCursor"]; time.sleep(0.2)
    return out
def main():
    ref = pd.read_csv(REF)
    rows=[]
    for _,r in ref.iterrows():
        nodes = fetch_org(r.get("tally_org"))
        if not nodes: 
            rows.append({"id":r["id"],"tally_proposals":None,"tally_votes":None}); continue
        df = pd.json_normalize(nodes)
        votes = df.get("votes").fillna(0).sum() if "votes" in df else 0
        rows.append({"id":r["id"],"tally_proposals":len(df),"tally_votes":int(votes)})
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("wrote", OUT)
if __name__=="__main__": main()
