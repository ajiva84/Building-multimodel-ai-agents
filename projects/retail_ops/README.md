# Project 2 — Retail Operations Agent (Chapter 16)

Two pipelines, one discipline: models read and draft; code validates;
humans hold every irreversible trigger.

- Invoices in: vision extract (per-field confidence) -> code validation
  (line-item math, known vendor, duplicate invoice number) -> gated Sheet
  post; anything low-confidence goes to a review queue WITH the image.
- Content out: draft -> critic with the brand checklist -> approval queue
  -> publish the exact approved payload.

Assemble from: ch08 (pipeline, critic), ch09 (escalation ladder),
ch12 (approval queue), ch11 (golden set = 20 of your real past invoices).
