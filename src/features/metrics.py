import numpy as np, pandas as pd
from src.utils.io import load_df, save_df

def compute():
    df = load_df('snapshot_spaces')
    df['turnout_rate_proxy'] = (df['proposalsCount'].replace(0,np.nan) / df['followersCount'].replace(0,np.nan)).clip(0,1)
    p = save_df(df, 'dao_metrics'); print(f'Wrote {p} rows={len(df)}')

if __name__=='__main__':
    compute()
