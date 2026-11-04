# Synthetic invoice JSON API

Use Python 3.12.3. Run `uv sync --locked --group dev`, then
`uv run --locked --offline pytest -q`. Start locally with
`uv run --locked uvicorn document_extraction.main:app --host 127.0.0.1 --port 8000`.

GET /health returns exactly {"status":"ok"}. POST /extract takes a strict
nonblank JSON text string up to 10,000 original characters, rejecting unknown
properties and invalid requests with 422. Response is exactly {"fields":{...}}
with invoice_number, date, total, currency always present. Missing/invalid values
are null. Labels match case-insensitively at line starts with whitespace and a
colon; first valid matching value wins. Invoice: [A-Za-z0-9-]{1,40}. Date: valid
YYYY-MM-DD calendar date. Total: nonnegative ASCII decimal, at most two fractional
digits, no exponent/separators, returned as a two-decimal string. Currency: three
ASCII letters, returned uppercase. Arbitrary nonempty text returns null fields.
Malformed JSON returns 422. No content execution, fetching, path use or logging.
Only synthetic text; no PDF, uploads, OCR, LLM, queues, auth, cloud or deployment.
