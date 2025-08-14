import matplotlib.pyplot as plt
from src.utils.io import load_df, REPORTS_FIGS

def main():
    df = load_df('dao_metrics')
    ax = df.boxplot(column='turnout_rate_proxy', by='gov_model', grid=False, rot=45)
    plt.title('Turnout (proxy) by Governance Model'); plt.suptitle('')
    plt.xlabel('Governance model'); plt.ylabel('Turnout rate (proxy)');
    out = REPORTS_FIGS / 'turnout_by_model.svg'
    plt.tight_layout(); plt.savefig(out)
    print(f'Saved {out}')

if __name__=='__main__':
    main()
