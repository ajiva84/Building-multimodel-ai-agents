"""Chapter 16 — the extraction contract."""
INVOICE_SCHEMA = {
  "vendor":      {"type": "string"},
  "invoice_no":  {"type": "string"},
  "date":        {"type": "string"},           # ISO
  "line_items":  {"type": "array"},            # {desc, qty, unit_price}
  "total":       {"type": "number"},
  "confidence":  {"type": "object"},           # per-field: high|medium|low
}

def validate(fields: dict) -> list:
    issues = []
    items = fields.get("line_items", [])
    calc = round(sum(i["qty"] * i["unit_price"] for i in items), 2)
    if abs(calc - fields.get("total", -1)) > 0.05:
        issues.append(f"totals mismatch: items sum {calc} vs {fields.get('total')}")
    conf = fields.get("confidence", {})
    lows = [k for k, v in conf.items() if v == "low"]
    if lows:
        issues.append(f"low confidence fields: {lows}")
    # plus: vendor in known list, invoice_no unseen (duplicate check)
    return issues
