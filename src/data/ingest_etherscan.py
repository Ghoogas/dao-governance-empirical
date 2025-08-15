import os, time, requests, pandas as pd
from pathlib import Path
KEY=os.getenv("ETHERSCAN_API_KEY")
OUT=Path("data/processed/etherscan_token.csv")
REF="data/reference/dao_ids.csv"
BASE="https://api.etherscan.io/api"
def holders(addr):
    if not KEY or not addr or pd.isna(addr): return None
    # Etherscan has no direct "holders" endpoint; use token supply as placeholder or skip.
    # Many fetch holders via third-party, but here we just return None to keep stub safe.
    return None
def main():
    ref=pd.read_csv(REF)
    rows=[{"id":r["id"], "token_holders": holders(r.get("token_address"))} for _,r in ref.iterrows()]
    pd.DataFrame(rows).to_csv(OUT, index=False)
    print("wrote", OUT)
if __name__=="__main__": main()
