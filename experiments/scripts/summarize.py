"""Validate an actual-run ledger and render counts; never infer missing usage."""

import argparse
import json
import math
from pathlib import Path

REQUIRED = {
    "run_id",
    "task_id",
    "arm",
    "start",
    "end",
    "elapsed_seconds",
    "hashes",
    "model",
    "runtime",
    "settings",
    "session",
    "environment",
    "status",
    "cases",
    "architecture",
    "interventions",
    "repair_iterations",
    "raw_log",
    "diff",
    "commands",
    "tokens",
    "tool_calls",
    "missing_reasons",
    "reviewer",
    "blinded",
    "exclusion_reason",
}


def validate(record):
    if not isinstance(record, dict) or REQUIRED - record.keys():
        raise ValueError("Missing ledger fields")
    if record["arm"] not in ("A", "B", "C") or record["task_id"] != "confidence":
        raise ValueError("Unknown arm/task")
    if record["status"] not in ("success", "failure", "timeout", "setup-failure"):
        raise ValueError("Unknown status")
    if not isinstance(record["run_id"], str) or not record["run_id"]:
        raise ValueError("Invalid run ID")
    from datetime import datetime

    start, end = [datetime.fromisoformat(record[k]) for k in ("start", "end")]
    if start.tzinfo is None or end.tzinfo is None or end < start:
        raise ValueError("Invalid timestamps")
    elapsed = record["elapsed_seconds"]
    if (
        isinstance(elapsed, bool)
        or not isinstance(elapsed, (int, float))
        or not math.isfinite(elapsed)
        or elapsed < 0
        or abs((end - start).total_seconds() - elapsed) > 1
    ):
        raise ValueError("Invalid elapsed duration")
    for key in ("hashes", "settings", "environment", "architecture", "missing_reasons"):
        if not isinstance(record[key], dict):
            raise ValueError(f"{key} must be an object")
    for key in ("cases", "interventions", "commands"):
        if not isinstance(record[key], list):
            raise ValueError(f"{key} must be a list")
    for key in ("starter", "overlay", "evaluator", "prompt", "lockfile", "candidate"):
        value = record["hashes"].get(key)
        if (
            not isinstance(value, str)
            or len(value) != 64
            or any(c not in "0123456789abcdef" for c in value)
        ):
            raise ValueError(f"Invalid {key} hash")
    for key in (
        "tokens",
        "tool_calls",
        "repair_iterations",
        "model",
        "runtime",
        "session",
        "raw_log",
        "diff",
    ):
        if record[key] is None and not record["missing_reasons"].get(key):
            raise ValueError(f"Unavailable {key} needs a reason")
    for case in record["cases"]:
        if (
            not isinstance(case, dict)
            or not isinstance(case.get("id"), str)
            or type(case.get("passed")) is not bool
        ):
            raise ValueError("Invalid per-case evidence")
    if record["status"] == "success" and (
        not record["cases"]
        or not all(c["passed"] for c in record["cases"])
        or record["architecture"].get("pass") is not True
        or not record["reviewer"]
    ):
        raise ValueError("Success lacks functional/manual architecture evidence")
    for key in ("raw_log", "diff"):
        if record[key] is not None and (
            Path(record[key]).is_absolute() or ".." in Path(record[key]).parts
        ):
            raise ValueError("Evidence paths must be relative")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    try:
        if args.output.exists():
            raise ValueError("Refusing to overwrite output; use a new path")
        rows = []
        ids = set()
        for line in args.input.read_text().splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            validate(record)
            if record["run_id"] in ids:
                raise ValueError("Duplicate run ID")
            ids.add(record["run_id"])
            rows.append(record)
        text = "# Trial results\n\n"
        if not rows:
            text += "Not run. Experiment prepared; agent trials not run.\n"
        else:
            text += (
                "Failures/timeouts/setup failures remain in denominators.\n\n"
                "| Arm | Functional | Architecture | Combined/attempts | Seconds |\n"
                "| --- | --- | --- | --- | --- |\n"
            )
            for arm in ("A", "B", "C"):
                selected = [r for r in rows if r["arm"] == arm]
                successes = sum(r["status"] == "success" for r in selected)
                seconds = sum(r["elapsed_seconds"] for r in selected)
                functional = sum(
                    bool(r["cases"]) and all(c["passed"] for c in r["cases"])
                    for r in selected
                )
                architecture = sum(
                    r["architecture"].get("pass") is True for r in selected
                )
                text += (
                    f"| {arm} | {functional} | {architecture} | "
                    f"{successes}/{len(selected)} | {seconds:.2f} |\n"
                )
            text += "\nExclusions (still retained above):\n"
            text += (
                "\n".join(
                    f"- {r['run_id']}: {r['exclusion_reason']}"
                    for r in rows
                    if r["exclusion_reason"]
                )
                or "None"
            )
            text += "\n\nMissing data:\n"
            text += (
                "\n".join(
                    f"- {r['run_id']}: "
                    f"{json.dumps(r['missing_reasons'], sort_keys=True)}"
                    for r in rows
                )
                + "\n"
            )
            text += (
                "\nNo cost estimate; usage and pricing were not joined.\n"
                "No significance claims.\n"
            )
        args.output.write_text(text)
        print(text)
    except (ValueError, OSError, TypeError, KeyError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    main()
