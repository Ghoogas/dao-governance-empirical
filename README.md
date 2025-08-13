# DAO Governance Empirical Study — Starter

Quick steps:
1) `python -m venv .venv && source .venv/bin/activate`
2) `pip install -r requirements.txt`
3) Copy `.env.example` to `.env` and fill keys.
4) Run:
   - `python -m src.data.ingest_snapshot`
   - `python -m src.features.metrics`
   - `python -m src.models.analysis`
   - `python -m src.viz.plots`
