"""Chapter 8 — the pipeline: fixed stages, models only where judgment lives."""

def process_invoice(pdf_text: str, extract_fields, validate,
                    write_journal_entry, queue_for_approval) -> dict:
    fields  = extract_fields(pdf_text)          # model, cheap tier
    issues  = validate(fields)                  # pure Python
    if issues:
        return {"status": "needs_human", "issues": issues, "fields": fields}
    entry   = write_journal_entry(fields)       # model, mid tier
    queue_for_approval(entry)                   # code (Ch. 12)
    return {"status": "queued", "entry": entry}
