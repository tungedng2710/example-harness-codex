"""Exercise utility refusal and bookkeeping, without launching agents."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parents[2]
SCRIPTS = ROOT / "experiments/scripts"


def invoke(name, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / name), *map(str, args)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_help_and_bad_candidate():
    for name in ["prepare_trial.py", "evaluate_trial.py", "summarize.py"]:
        assert invoke(name, "--help").returncode == 0
    assert (
        invoke(
            "evaluate_trial.py", "--candidate", "/missing", "--expect", "pass"
        ).returncode
        != 0
    )


def test_prepare_preserves_nonempty(tmp_path):
    destination = tmp_path / "trial"
    destination.mkdir()
    marker = destination / "keep"
    marker.write_text("preserve")
    assert (
        invoke("prepare_trial.py", "--arm", "A", "--out", destination).returncode != 0
    )
    assert marker.read_text() == "preserve"


def test_prepare_common_hashes(tmp_path):
    common = None
    for arm in ["A", "B", "C"]:
        destination = tmp_path / arm
        assert (
            invoke("prepare_trial.py", "--arm", arm, "--out", destination).returncode
            == 0
        )
        metadata = json.loads((destination / "trial-input-manifest.json").read_text())
        if common is None:
            common = metadata["common"]
        assert metadata["common"] == common
        assert (destination / "AGENTS.md").exists() is (arm != "A")
        assert not (destination / "experiments/evaluator").exists()


def test_summary_empty_and_malformed(tmp_path):
    ledger = tmp_path / "runs.jsonl"
    ledger.write_text("")
    output = tmp_path / "summary.md"
    assert invoke("summarize.py", "--input", ledger, "--output", output).returncode == 0
    assert "Not run" in output.read_text()
    assert invoke("summarize.py", "--input", ledger, "--output", output).returncode != 0
    ledger.write_text('{"arm":"A"}\n')
    assert (
        invoke(
            "summarize.py", "--input", ledger, "--output", tmp_path / "bad.md"
        ).returncode
        != 0
    )
