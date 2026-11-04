#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
uv run --locked --offline ruff check .
uv run --locked --offline ruff format --check .
uv run --locked --offline pytest -q
uv run --locked --offline python scripts/check_architecture.py
uv run --locked --offline python scripts/smoke.py
