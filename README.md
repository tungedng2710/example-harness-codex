# Harness engineering demo

A local, deterministic FastAPI service for synthetic invoice text. No GPU, model,
API key or database. This repository demonstrates engineering practices around a
coding agent; effectiveness is a hypothesis. **Experiment prepared; agent trials
not run.** See the [article](docs/blog/harness-engineering-with-codex.md) and
[protocol](experiments/README.md).

## Setup

Use Python 3.12.3 and uv (tested: 0.13.7). Install uv using its official package or
installer after reviewing it; no global tooling is required. On this host a local
bootstrap used `python3 -m pip install --target .tooling-packages uv`; prepend
`$PWD/.tooling-packages/bin` to PATH if using that approach.

```bash
uv sync --locked --group dev
bash scripts/check.sh
uv run --locked uvicorn document_extraction.main:app --host 127.0.0.1 --port 8000
```

In another terminal:

```bash
curl --fail-with-body http://127.0.0.1:8000/health
curl --fail-with-body http://127.0.0.1:8000/extract \
  -H 'Content-Type: application/json' \
  --data '{"text":"Invoice Number: INV-001\nDate: 2026-01-15\nTotal: 123.45\nCurrency: usd","include_confidence":true}'
```

Health returns exactly `{"status":"ok"}`. Extraction returns:

```json
{"fields":{"invoice_number":"INV-001","date":"2026-01-15","total":"123.45","currency":"USD"},"confidence":{"invoice_number":1.0,"date":1.0,"total":1.0,"currency":1.0}}
```

Omit the flag or pass false to receive only `fields`. Scores are rule-based
presence/validity indicators, not probabilities, model certainty or accuracy.
All four field keys are present; invalid/missing values are null. The first valid
matching labeled line wins. See [architecture](docs/architecture.md) and
[conventions](docs/conventions.md). Invoke `$api-review` for the repository review
skill; file creation alone does not guarantee invocation.

Only JSON text is supported: strict nonblank string, original length ≤10,000,
strict boolean flag and no unknown properties. Invalid requests return 422.
This is not a general invoice parser: no PDFs, uploads, OCR, LLM inference, queues,
authentication, cloud infrastructure or deployment. Never use customer documents.
Content is never executed, fetched, used as a path, or logged by application code.

The check script runs offline lint, format verification, public tests, static
architecture checks and in-process TestClient smoke checks. It does not format
files. Expected warning: current Starlette deprecates HTTPX-backed TestClient;
HTTPX is retained because the brief requires it, and tests verify behavior.
Dependency installation needs network access on a clean machine; checks use caches.

See [implementation evidence](docs/implementation-log.md),
[environment versions](docs/environment.json), and [verified sources](docs/sources.md).
No service or website has been published.
