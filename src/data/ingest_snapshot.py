import os, requests, pandas as pd
from src.utils.io import save_df
from src.utils.labels import label_governance_model

GRAPHQL = os.getenv('SNAPSHOT_GRAPHQL', 'https://hub.snapshot.org/graphql')

Q = """
query($first:Int!,$skip:Int!){
  spaces(first:$first, skip:$skip, where:{verified:true}){
    id name about network followersCount proposalsCount
  }
}
"""

def gql(query, variables=None):
    r = requests.post(GRAPHQL, json={'query': query, 'variables': variables or {}}, timeout=60)
    r.raise_for_status(); return r.json()['data']

def main():
    spaces=[]
    for skip in range(0,5000,1000):
        d=gql(Q, {'first':1000,'skip':skip})['spaces']
        if not d: break
        spaces.extend(d)
    df = pd.json_normalize(spaces)
    df['gov_model'] = df.apply(lambda r: label_governance_model(r.to_dict()), axis=1)
    p = save_df(df, 'snapshot_spaces'); print(f'Wrote {p} rows={len(df)}')

if __name__=='__main__':
    main()
