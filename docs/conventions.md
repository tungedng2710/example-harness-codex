# Conventions

Strict JSON requests; forbid unknown properties. Preserve original text length.
Never log document content. Missing or invalid fields are null; select first valid
line. Only ASCII numeric grammar is accepted. Use Decimal for totals. Keep HTTP
out of the use case. Offline checks never format or repair files.

Inspect → implement → targeted verification → repair → full verification.
Stop after three consecutive failed repairs for the same issue. Report failures
and incomplete checks. Explicit repairs: `uv run --locked --offline ruff check --fix .`
and `uv run --locked --offline ruff format .`. Never weaken tests to pass.
