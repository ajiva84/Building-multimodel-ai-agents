"""Chapter 7 — hybrid search: vector + keyword, merged by RRF."""

def hybrid_search(vector_search, keyword_search, query: str, k: int = 5):
    """Reciprocal Rank Fusion: reward showing up high in either list.
    vector_search / keyword_search: callables returning ranked hit lists,
    each hit having an .id attribute (or adapt to your stores)."""
    vec_hits = vector_search(query, k=20)      # semantic
    kw_hits  = keyword_search(query, k=20)     # exact identifiers (BM25/FTS)
    scores = {}
    for rank, hit in enumerate(vec_hits):
        scores[hit.id] = scores.get(hit.id, 0) + 1 / (60 + rank)
    for rank, hit in enumerate(kw_hits):
        scores[hit.id] = scores.get(hit.id, 0) + 1 / (60 + rank)
    return sorted(scores, key=scores.get, reverse=True)[:k]
