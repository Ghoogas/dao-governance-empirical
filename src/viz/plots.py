import matplotlib.pyplot as plt
from src.utils.io import load_df, REPORTS

def main():
    df = load_df('dao_metrics')
    ax = df.boxplot(column='turnout_rate_proxy', by='gov_model', grid=False, rot=45)
    plt.title('Turnout (proxy) by Governance Model'); plt.suptitle('')
    plt.xlabel('Governance model'); plt.ylabel('Turnout rate (proxy)');
    out = REPORTS/'figures'/'turnout_by_model.png'
    plt.tight_layout(); plt.savefig(out, dpi=150); print(f'Saved {out}')

if __name__=='__main__':
    main()
