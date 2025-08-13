import statsmodels.formula.api as smf
from src.utils.io import load_df, REPORTS

def run():
    df = load_df('dao_metrics').dropna(subset=['turnout_rate_proxy'])
    df['gov_model'] = df['gov_model'].astype('category')
    m = smf.ols('turnout_rate_proxy ~ C(gov_model)', data=df).fit(cov_type='HC3')
    out = REPORTS/'tables'/'ols_turnout_by_model.txt'
    out.write_text(m.summary().as_text())
    print(f'Wrote {out}')

if __name__=='__main__':
    run()
