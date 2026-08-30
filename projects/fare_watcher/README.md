# Project 1 — The Flight-Price Watcher (Chapter 15)

Watches routes you care about, re-checks fares with FRESH data when a feed
reports a change, and lets a code gate — never the model — decide whether an
alert is sent.

Assemble from: ch14 (receiver/worker), ch04 (tools), ch05 (loop),
ch06 (state object with `alert_sent` + dedupe key), ch12 (alert gate that
RE-FETCHES the live fare), ch11 (golden set with 10 should-NOT-alert cases).

Tools: get_fare · get_seats · price_history · log_check

Build order and hardening checklist: Chapter 15.

NOTE: if you extend this to auto-booking, that action is irreversible and
spends real money. Human approval only (Ch. 12) — no exceptions.
