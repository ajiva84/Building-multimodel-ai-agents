"""Chapter 9 — the escalation ladder: cheap first, promote on checkable failure."""
from tiers import MODELS

def extract_with_escalation(extract, doc: str) -> dict:
    """extract(model, doc) -> dict with 'confidence', or None on failure."""
    for model in [MODELS["extract"], MODELS["act"], MODELS["plan"]]:
        result = extract(model, doc)
        if result and result.get("confidence") != "low":
            result["_model_used"] = model          # log it — routing is arithmetic
            return result
    return {"status": "needs_human", "doc_ref": hash(doc)}
