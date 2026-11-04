# Synthetic invoice extraction

Implement the assigned confidence feature only. Preserve exact legacy JSON for
omitted/false flags and strict validation. Never execute document content.
HTTP API → service → deterministic extractor; shared schemas have no upward
imports. Read docs/architecture.md when changing boundaries. Routes delegate;
services cannot import API/FastAPI/Starlette, inference cannot import services or
HTTP, and schemas cannot import API/services/inference.

Verify from the root:
- `uv run --locked --offline pytest -q`
- `uv run --locked --offline ruff check .`
- `uv run --locked --offline ruff format --check .`

Report changed files, commands, exit statuses and remaining failures. Never
weaken tests or claim verification that did not run. Keep scope to JSON text;
no network, OCR, inference services or deployment.

Inspect → implement → targeted check → repair → full check. Run
`bash scripts/check.sh` before completion. Use `.agents/skills/api-review/SKILL.md`
(explicit invocation `$api-review`) after API changes. Inspect route delegation
manually. Stop after three consecutive failed repairs on the same issue, or the
15-minute trial timeout. Report evidence and unresolved work; do not weaken checks.
