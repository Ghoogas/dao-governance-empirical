import numpy as np, pandas as pd
from src.utils.io import load_df, save_df

def compute():
    df = load_df('snapshot_spaces')
    # basic metrics
    df['turnout_rate_proxy'] = (
        df['proposalsCount'].replace(0, np.nan) / df['followersCount'].replace(0, np.nan)
    ).clip(0, 1)
    df['log_followers'] = np.log1p(df['followersCount'].fillna(0))
    if 'treasuryUSD' in df.columns:
        df['log_treasury'] = np.log1p(df['treasuryUSD'].fillna(0))
    # Merge DefiLlama treasury (optional)
    try:
        llama = pd.read_csv('data/processed/defillama_treasury.csv')
        if 'treasuryUSD' in llama.columns:
            df = df.merge(llama[['id', 'treasuryUSD']], on='id', how='left', suffixes=('', '_ll'))
            df['treasuryUSD'] = df['treasuryUSD'].fillna(df.get('treasuryUSD_ll'))
            df.drop(columns=[c for c in df.columns if c.endswith('_ll')], inplace=True, errors='ignore')
            df['log_treasury'] = np.log1p(df['treasuryUSD'].fillna(0))
    except FileNotFoundError:
        pass
    # Merge Tally (optional)
    try:
        tally = pd.read_csv('data/processed/tally_gov.csv')
        df = df.merge(tally, on='id', how='left')
    except FileNotFoundError:
        pass
    # Merge Dune/Etherscan/Snapshot activity (optional)
    for p in ['data/processed/dune_metrics.csv', 'data/processed/etherscan_token.csv', 'data/processed/snapshot_activity_90d.csv']:
        try:
            extra = pd.read_csv(p)
            df = df.merge(extra, on='id', how='left')
        except FileNotFoundError:
            pass
    p = save_df(df, 'dao_metrics')
    print(f'Wrote {p} rows={len(df)}')

if __name__ == '__main__':
    compute()
