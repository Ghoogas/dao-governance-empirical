from pathlib import Path
import pandas as pd

DATA = Path('data'); (DATA/'processed').mkdir(parents=True, exist_ok=True)
REPORTS = Path('reports'); (REPORTS/'tables').mkdir(parents=True, exist_ok=True); (REPORTS/'figures').mkdir(parents=True, exist_ok=True)

def save_df(df, name):
    p = DATA/'processed'/f"{name}.csv"; df.to_csv(p, index=False); return p
def load_df(name):
    p = DATA/'processed'/f"{name}.csv"; return pd.read_csv(p)
