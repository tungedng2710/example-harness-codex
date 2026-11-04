"""Score a disposable copy in its own locked environment; never invoke Codex."""

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

from common import EXPERIMENTS, ROOT, digest, manifest, verify_freeze


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--expect", required=True, choices=["pass", "feature-failure"])
    parser.add_argument(
        "--output", type=Path, help="New JSON evidence file outside candidate"
    )
    args = parser.parse_args()
    try:
        frozen = verify_freeze()
        candidate = args.candidate.resolve(strict=True)
        if not (candidate / "src/document_extraction/main.py").is_file():
            raise ValueError("Candidate source package missing")
        if args.output:
            output = args.output.resolve()
            if output.exists() or output == candidate or candidate in output.parents:
                raise ValueError("Output must be new and outside candidate")
        before = (
            manifest(candidate) if candidate != ROOT else manifest(candidate / "src")
        )
        # Reject modifications to frozen public tests, dependencies and C check tools.
        for name, expected in frozen["starter"].items():
            if name.startswith("tests/") or name in {
                "pyproject.toml",
                "uv.lock",
                ".python-version",
            }:
                path = candidate / name
                if not path.is_file() or manifest_file(path) != expected:
                    raise ValueError(f"Protected input altered: {name}")
        for name, expected in frozen["overlays/C"].items():
            if name.startswith("scripts/") and (candidate / name).exists():
                if manifest_file(candidate / name) != expected:
                    raise ValueError(f"Harness setting altered: {name}")
        commands = []
        cases = []
        with tempfile.TemporaryDirectory(prefix="harness-evaluation-") as directory:
            work = Path(directory)
            snapshot = work / "candidate"
            snapshot.mkdir()
            for name in ["src", "pyproject.toml", "uv.lock", ".python-version"]:
                source = candidate / name
                if source.is_dir():
                    shutil.copytree(
                        source,
                        snapshot / name,
                        ignore=shutil.ignore_patterns("__pycache__"),
                    )
                else:
                    shutil.copy2(source, snapshot / name)
            env = os.environ.copy()
            env.pop("PYTHONPATH", None)
            env.pop("VIRTUAL_ENV", None)

            def run(command):
                result = subprocess.run(
                    command,
                    cwd=snapshot,
                    env=env,
                    text=True,
                    capture_output=True,
                    timeout=120,
                )
                commands.append(
                    {
                        "command": command,
                        "exit_code": result.returncode,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                    }
                )
                return result

            setup = run(["uv", "sync", "--locked", "--offline", "--group", "dev"])
            if setup.returncode:
                raise ValueError(f"Candidate setup failed: {setup.stderr}")
            python = str(snapshot / ".venv/bin/python")
            provenance = run(
                [
                    python,
                    "-c",
                    "import document_extraction; print(document_extraction.__file__)",
                ]
            )
            if provenance.returncode or not provenance.stdout.strip().startswith(
                str(snapshot / "src") + "/"
            ):
                raise ValueError("Wrong module provenance")
            for category, suite in [
                ("regression", EXPERIMENTS / "starter/tests"),
                ("feature", EXPERIMENTS / "evaluator"),
            ]:
                # Copy fixed suites outside the candidate.
                suite_copy = work / category
                shutil.copytree(suite, suite_copy / "tests")
                if category == "regression":
                    shutil.copytree(
                        EXPERIMENTS / "overlays/C/scripts", suite_copy / "scripts"
                    )
                report = work / f"{category}.xml"
                result = run(
                    [
                        python,
                        "-m",
                        "pytest",
                        str(suite_copy / "tests"),
                        "-q",
                        "-p",
                        "no:cacheprovider",
                        "--junitxml",
                        str(report),
                        "-c",
                        str(snapshot / "pyproject.toml"),
                    ]
                )
                if result.returncode not in (0, 1) or not report.exists():
                    raise ValueError(
                        f"{category} collection/runtime failure: "
                        f"{result.stderr} {result.stdout}"
                    )
                nodes = ET.parse(report).getroot().findall(".//testcase")
                if not nodes or any(
                    node.find("error") is not None or node.find("skipped") is not None
                    for node in nodes
                ):
                    raise ValueError(f"{category} incomplete or setup errors")
                cases.extend(
                    {
                        "category": category,
                        "id": node.attrib["classname"] + "." + node.attrib["name"],
                        "passed": node.find("failure") is None,
                    }
                    for node in nodes
                )
            architecture = run(
                [
                    python,
                    str(ROOT / "scripts/check_architecture.py"),
                    "--source",
                    str(snapshot / "src/document_extraction"),
                ]
            )
        regression_ok = all(c["passed"] for c in cases if c["category"] == "regression")
        feature_ok = all(c["passed"] for c in cases if c["category"] == "feature")
        designated = [c for c in cases if "test_feature_" in c["id"]]
        expected_failure = (
            regression_ok
            and bool(designated)
            and all(not c["passed"] for c in designated)
            and all(c["passed"] for c in cases if "test_bad_flags" in c["id"])
        )
        accepted = (
            regression_ok and feature_ok if args.expect == "pass" else expected_failure
        )
        accepted = accepted and architecture.returncode == 0
        evidence = {
            "kind": "evaluator-output",
            "candidate": str(candidate),
            "candidate_hash": digest(before),
            "frozen_hash": digest(frozen),
            "cases": cases,
            "functional_pass": regression_ok and feature_ok,
            "architecture_imports_pass": architecture.returncode == 0,
            "manual_rubric": "pending; required for trial success",
            "expectation_met": accepted,
            "commands": commands,
        }
        if args.output:
            args.output.write_text(json.dumps(evidence, indent=2) + "\n")
        print(
            json.dumps(
                {k: v for k, v in evidence.items() if k not in {"cases", "commands"}},
                indent=2,
            )
        )
        print(f"Cases: {sum(c['passed'] for c in cases)}/{len(cases)}")
        return 0 if accepted else 1
    except (ValueError, OSError, subprocess.TimeoutExpired) as error:
        parser.exit(2, f"{error}\n")


def manifest_file(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
