# Prepared experiment — no agent trials run

The frozen starter predates confidence. `manifests.json` freezes its files,
B/C overlays, evaluator, common prompt and protocol. Preparation verifies these
hashes and common-file equality. The construction brief, article, final solution
and evaluator are never copied into trials. A has ordinary README and public
functional tests; B adds concise instructions and architecture; C adds the skill,
architecture/smoke/check scripts and feedback guidance. Extra architecture feedback
is a declared bundled treatment, not a single-component ablation. All arms retain
the Codex runtime, normal tools and safety controls. A/B may run tests and repair.

## Local reproduction, without an agent

From the repository root with uv on PATH:

```bash
uv run --locked python experiments/scripts/evaluate_trial.py --candidate experiments/starter --expect feature-failure
uv run --locked python experiments/scripts/evaluate_trial.py --candidate . --expect pass
TRIAL_ROOT=$(mktemp -d /tmp/harness-trials.XXXXXX)
uv run --locked python experiments/scripts/prepare_trial.py --arm A --out "$TRIAL_ROOT/A-01"
uv run --locked python experiments/scripts/prepare_trial.py --arm B --out "$TRIAL_ROOT/B-01"
uv run --locked python experiments/scripts/prepare_trial.py --arm C --out "$TRIAL_ROOT/C-01"
uv run --locked python experiments/scripts/summarize.py --input experiments/results/runs.jsonl --output experiments/results/summary.md
```

Summary refuses an existing output. Preserve prior evidence and choose a new
output path when rerunning. All three utilities offer --help and reject bad paths.
Preparation rejects nonempty directories and locations inside this repository.
The evaluator makes a disposable source copy, installs its locked dependencies
with offline uv, verifies module provenance, and runs fixed external tests with
that environment's Python. It never invokes Codex or changes candidate files.
Use `--output /tmp/new-evaluation.json` to preserve command exits, output and
per-case results. Expected-feature-failure accepts only passing regressions and
all designated new-feature assertions failing; setup/collection errors are errors.
Self-checks do not create trial ledger rows. Evaluator output is not combined
trial success until the fixed manual architecture rubric is reviewed.

## Fresh sessions: manual operator procedure (requires separate authorization)

Local `codex --help`, `codex exec --help`, and `codex --version` were inspected:
version 0.166.0. Official [CLI reference](https://learn.chatgpt.com/docs/cli/reference)
was opened. The following interactive launch syntax is supported locally:

```bash
codex -C "$TRIAL_ROOT/A-01"
```

This command has NOT been executed. Use a fresh session for each arm and paste
exactly `experiments/tasks/confidence.md` as the task, without chat history or
other results. Initialize each trial with `git init` and a starter commit before
launch, so changes can be retained as a sanitized diff. Install the frozen lock
before timing: `(cd "$TRIAL_ROOT/A-01" && uv sync --locked --group dev)`.
Do not launch from this repository, use resume/fork, or pass the construction
brief. Do not copy credentials or modify global configuration.

Before the first trial, freeze exact model identifier, reasoning setting, CLI
version, tools, hardware, permissions and network policy in a separate dated
execution-settings artifact. Protocol nulls are unresolved settings, not defaults.
Keep that artifact identical across attempts; its hash belongs in each record.
The local CLI offers --profile, but its help describes layering over base user
configuration; it does not by itself establish isolation. Although exec advertises
--ignore-user-config, that does not prove isolation from global skills, plugins,
memories or inherited instructions. Inspect effective guidance and record those
sources for every trial. No supported fully isolated profile has been established
by this build. If that remains unresolved, label trials confounded. Never disable
approvals or change permission controls to improve comparability.

Keep evaluator files outside agent-accessible paths using a separately restricted
account/container/filesystem when available. This build has unrestricted filesystem
access and establishes no privacy barrier. A different /tmp directory alone is
not a barrier. If privacy cannot be enforced, call the evaluator agent-visible.
Do not claim hidden tests. No container or privileged setup is a prerequisite for
using the local teaching service.

Use the frozen interleaving A/B/C, B/C/A, C/A/B (three repetitions per arm). Time
setup separately; give each run 900 seconds and at most three repairs. For manual
interactive runs the operator must monitor time, interrupt at the limit and record
actual repair counts; this repository does not enforce the runtime limit. Record
unobservable counts as null with a reason and deviations explicitly. No semantic
hints or source edits; record permission prompts separately. If assistance occurs,
preserve the unassisted outcome before a separately labeled continuation.

After the agent stops, retain a candidate snapshot without modifying it and run:

```bash
uv run --locked python experiments/scripts/evaluate_trial.py --candidate "$TRIAL_ROOT/A-01" --expect pass --output /tmp/A-01-evaluation.json
```

Do not feed evaluation back for a scored repair. Post-evaluation fixes are separate
demonstrations. The evaluator rejects changed frozen public tests, dependency
settings and existing C check scripts rather than silently repairing them.

## Scoring and evidence ledger

Functional correctness means every fixed regression and feature case passes.
Architecture is reported separately: static import result plus manual inspection
of route delegation, unrelated changes and test weakening using objective rules
in protocol.json. Record reviewer identity and blinding. A reviewer who sees the
skill or scripts is likely unblinded; disclose that. Combined success requires
both functional and architecture success. Each finding needs path, line and reason.

Append one JSON object per attempted run to results/runs.jsonl, including failed,
timed-out and setup-failed attempts. The schema is the REQUIRED set and validate()
in scripts/summarize.py. Obtain start/end from a real clock; derive elapsed;
copy per-case results and commands from evaluator output, hashes from frozen
manifests/input manifests and saved candidate tree. Hash candidate using common.py
manifest()+digest(), not Git status alone. A's empty overlay hash is digest({}).
Never invent measurements to fill a schema. Unknown tokens, tool calls, session
IDs, model or repair counts must be null with missing_reasons entries. Model and
runtime settings must come from actual session evidence. Store relative sanitized
log/diff paths, setup duration in environment, interventions as observed records,
architecture findings, reviewer and whether blinded. Do not store credentials.

The ledger requires run_id, task_id, arm, start, end, elapsed_seconds, hashes
(starter/overlay/evaluator/prompt/lockfile/candidate), model, runtime, settings,
session, environment, status, cases, architecture, interventions, repair_iterations,
raw_log, diff, commands, tokens, tool_calls, missing_reasons, reviewer, blinded and
exclusion_reason. Allowed status: success/failure/timeout/setup-failure. cases use
{id, passed}. architecture needs pass:true for success. Use null exclusion_reason
when none. Include settings isolation deviations explicitly. Validate the entire
ledger by generating a new summary before accepting it; validation rejects duplicate
IDs and malformed rows. If validation fails, retain the original evidence, correct
transcription against source evidence, and validate again. An empty ledger is valid.

Summary retains unsuccessful attempts in denominators and shows total elapsed
including failures. Exclusions and missing data remain visible. No cost is computed
without reliable usage and dated cited pricing. Nine runs on one synthetic task
cannot establish significance, model-wide superiority or production safety.
