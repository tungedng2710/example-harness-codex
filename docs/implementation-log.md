# Implementation log

## Plan (not execution evidence)

Build the strict JSON-only starter; verify with Python 3.12 and uv. Freeze starter,
public tests, evaluator, prompt, scoring and overlays with SHA-256 manifests before
adding optional confidence. Run targeted checks, full offline checks, evaluator
self-checks, preparation commands and API review. Write the article against files
and recorded evidence. No additional agent trials are authorized.

Acceptance: exact legacy JSON shape, strict input, deterministic first-valid-line
extraction, neutral service boundaries, reproducible isolated candidate evaluation,
and honest separation of local checks from unrun A/B/C trials.

## Execution

- Initial directory: only AGENTS.md; no Git repository. Brief preserved.
- Shell Python: 3.13.15; discovered required /usr/bin/python3.12: 3.12.3.
- uv absent from PATH. Python 3.12 venv bootstrap failed (ensurepip missing).
  Trying pip package installation into ignored project-local .tooling-packages;
  no global installation or configuration changes.

- Project-local uv 0.13.7 installed successfully with pip --target; resolved lock
  and synced dependencies using CPython 3.12.3. No stack substitution.
- Starter `bash scripts/check.sh`: exit 0, 46 tests passed, import and smoke
  checks passed. Initial check failed on long lines; explicit formatting and
  splitting long strings fixed it. This was a real construction lint failure,
  not a staged defect. HTTPX TestClient emits a deprecation warning.
- Frozen source/public tests/lock/prompt/evaluator/protocol/B/C overlays saved
  before confidence implementation. `experiments/manifests.json` holds hashes.
- First manifest validation failed because the ad-hoc freeze included a Python
  cache while the validator excludes caches. Rebuilt the manifest consistently
  before implementing confidence; no source or acceptance behavior changed.

- Frozen starter evaluator self-check: exit 0 with --expect feature-failure;
  45/49 assertions pass, exactly four designated feature assertions fail.
  Fixed regressions and bad-flag rejection pass. See starter-evaluator.json.
- Confidence implemented only in final schemas/service/route. Targeted integration
  run: exit 0, 26 tests passed. Explicit formatting repaired newly written long
  lines. No intentional teaching defects were inserted.
- Final evaluator self-check: exit 0 with --expect pass, 49/49 cases pass,
  static imports pass. See final-evaluator.json. This evaluates application source;
  subsequent changes added utility/debug-logging tests and summary reporting only.
- prepare_trial.py A/B/C commands: exit 0, disposable roots under
  /tmp/harness-trials.WNmV2m; common hashes matched. These inputs are not agent runs.
  No Codex trial sessions launched. Temporary trial paths are not durable artifacts.
- summarize.py on empty ledger: exit 0; results/summary.md says Not run.
  --help, bad candidate, nonempty destination, common input equality, empty and
  malformed summary behavior also covered by unit checks.
- Skill validator in project Python initially failed because its optional PyYAML
  dependency was missing. Running that tooling-only validator with the host Python
  succeeded: "Skill is valid!" Application tests still use Python 3.12.3.
- API review skill explicitly read/applied in this construction. Reviewer: root
  Codex construction agent, unblinded; not an independent assessment. Compared
  starter/final source diff: route only forwards flag; service computes scores;
  strict validation and original-length behavior preserved; null fields retained.
  Frozen public tests and harness settings unchanged. No unresolved substantive
  API findings. Added DEBUG-level logging/captured-output coverage because the
  starter log assertion alone used default log capture level.
- Final `bash scripts/check.sh`: recorded in final-check-output.txt; exit 0,
  62 tests pass, Ruff lint/format, static architecture and smoke pass offline.
  This run follows the last code change. Source/test/tool hashes and aggregate
  SHA-256 are in verified-tree.json; no Git revision exists in this initial folder.
- Live Uvicorn command at 127.0.0.1:8000: exit 3 (port already occupied).
  Existing process left untouched. Retried at 127.0.0.1:8765: startup successful;
  curl --fail-with-body health and complete confidence extraction both exit 0,
  HTTP 200, exact documented JSON. Stopped only the server started by this build
  with Ctrl-C; its shutdown exit was 130. No server remains from this build.
- Article check: exit 0; 2,708 words, all relative links resolve, copied service
  and check commands match final files, exactly two Mermaid diagrams.
- Official HTML references opened at build time; see sources.md. No price or
  performance claims copied from external benchmark examples.

## Handoff and limits

README and article are complete. Frozen inputs, protocol, validated utilities and
empty ledger are present. Local mandatory checks passed. Current HTTPX-backed
TestClient emits a deprecation warning; no extra HTTP client dependency was added.
No trial outcomes, deployment, publication, token usage or cost are claimed.
Runtime guidance isolation, evaluator privacy, exact model/reasoning/tool settings
and manual trial reviewers remain to be established before any authorized trials;
these are preparation limitations, not completed execution evidence. Python 3.12.3
and a uv installation plus dependency network access are clean-checkout prerequisites.
