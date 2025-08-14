from pathlib import Path
import pandas as pd

DATA = Path('data'); (DATA/'processed').mkdir(parents=True, exist_ok=True)
REPORTS = Path('reports')
REPORTS_TABLES = REPORTS / 'tables'; REPORTS_TABLES.mkdir(parents=True, exist_ok=True)
REPORTS_FIGS = REPORTS / 'figures'; REPORTS_FIGS.mkdir(parents=True, exist_ok=True)

def save_df(df, name):
    p = DATA/'processed'/f"{name}.csv"; df.to_csv(p, index=False); return p
def load_df(name):
    p = DATA/'processed'/f"{name}.csv"; return pd.read_csv(p)
