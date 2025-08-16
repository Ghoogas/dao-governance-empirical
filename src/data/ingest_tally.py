import os, time, requests

API = "https://api.tally.xyz/query"

# Simple, paginated pull of proposals for an org slug
def fetch_org(slug: str, limit: int = 100):
    key = os.getenv("TALLY_API_KEY")
    if not key:
        raise RuntimeError("TALLY_API_KEY not set")

    headers = {
        "Api-Key": key,                    # <-- exact header Tally expects
        "Content-Type": "application/json",
    }

    query = """
    query Proposals($slug: String!, $limit: Int, $cursor: String) {
      proposals(organization: { slug: $slug }, limit: $limit, after: $cursor) {
        pageInfo { endCursor hasNextPage }
        nodes { id title state quorum createdAt votes { for against abstain } }
      }
    }
    """

    out, cursor = [], None
    while True:
        payload = {"query": query, "variables": {"slug": slug, "limit": limit, "cursor": cursor}}
        r = requests.post(API, headers=headers, json=payload)
        if r.status_code != 200:
            print(f"[tally] {slug} HTTP {r.status_code}: {r.text[:500]}")
            # break early on hard errors (422/401), back off on 429
            if r.status_code == 429:
                time.sleep(1.0)
                continue
            break
        try:
            data = r.json()
        except Exception:
            print(f"[tally] {slug} non-JSON response: {r.text[:500]}")
            break

        # GraphQL errors block is explicit
        if "errors" in data and data["errors"]:
            print(f"[tally] {slug} GraphQL errors: {data['errors']}")
            break

        proposals = data.get("data", {}).get("proposals", {})
        nodes = proposals.get("nodes", []) or []
        out.extend(nodes)
        info = proposals.get("pageInfo", {}) or {}
        if info.get("hasNextPage"):
            cursor = info.get("endCursor")
            time.sleep(0.2)
            continue
        break

    return out

