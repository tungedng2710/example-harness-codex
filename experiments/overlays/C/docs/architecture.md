# Boundaries

HTTP API → extraction service → deterministic extractor. All may use schemas.
`main.py` explicitly assembles the app and router. Routes only validate, delegate,
and serialize. Services cannot import API, FastAPI or Starlette. Inference cannot
import those or services. Schemas cannot import API, services or inference.
Pydantic field results are framework-neutral (no HTTP framework dependency).

The checker resolves static absolute and relative import edges in the selected
`src/document_extraction` package. It does not scan every experiment snapshot.
It cannot prove route delegation, detect all dynamic imports, aliases loaded via
runtime mechanisms, semantic business logic, or malicious code. Review the diff
and routes manually. No dynamic imports are needed in application code.
