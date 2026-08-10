# Project 1 — Market-Monitoring Alert Agent (Chapter 15)

Receives TradingView webhooks, re-analyzes with FRESH data, and only a
code gate — never the model — decides whether an alert is sent.

Assemble from: ch14 (receiver/worker), ch04 (tools), ch05 (loop),
ch06 (state object with `alert_sent` + dedupe key), ch12 (alert gate
that RECOMPUTES the score), ch11 (golden set with 10 should-NOT-alert cases).

Build order and hardening checklist: Chapter 15.
