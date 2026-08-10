"""Chapter 17 — the findings contract: the seam that makes reports honest."""
EXAMPLE_FINDINGS = {
  "question": "...",
  "claims": [
    {"text": "Vendor financing at 30-day terms typically costs 1.5-2%/mo",
     "source": "https://...",
     "quote": "the sentence that supports it, verbatim",
     "confidence": "medium"}
  ],
  "dead_ends": ["searched X, found nothing recent"]
}

def validate_findings(f: dict) -> list:
    issues = []
    for i, c in enumerate(f.get("claims", [])):
        for field in ("text", "source", "quote", "confidence"):
            if not c.get(field):
                issues.append(f"claim {i}: missing {field}")
    return issues
