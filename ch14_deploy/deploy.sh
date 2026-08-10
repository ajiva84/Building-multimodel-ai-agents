#!/bin/bash
# The only way code reaches the VPS. Prompts are code; edits pass the gate.
set -e
python ch11_evals/run_evals.py --set ch11_evals/golden --runs 3 --min-pass 0.85
rsync -a . vps:/opt/agent/
ssh vps 'systemctl restart agent-worker'
