"""Shared deterministic experiment bookkeeping."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = ROOT / "experiments"


def manifest(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(root.rglob("*"))
        if p.is_file()
        and not any(
            part in {".venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".git"}
            for part in p.relative_to(root).parts
        )
    }


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def verify_freeze() -> dict:
    frozen = json.loads((EXPERIMENTS / "manifests.json").read_text())
    for name, hashes in frozen.items():
        path = EXPERIMENTS / name
        actual = (
            manifest(path)
            if path.is_dir()
            else {path.name: hashlib.sha256(path.read_bytes()).hexdigest()}
        )
        if actual != hashes:
            raise ValueError(f"Frozen artifact changed: {name}")
    return frozen
