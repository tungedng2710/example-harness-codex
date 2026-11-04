"""Prepare frozen inputs only; never launch an agent."""

import argparse
import json
import shutil
from pathlib import Path

from common import EXPERIMENTS, ROOT, digest, manifest, verify_freeze


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--arm", required=True, choices=["A", "B", "C"])
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        frozen = verify_freeze()
        out = args.out.resolve()
        if out == ROOT or ROOT in out.parents or out in ROOT.parents:
            raise ValueError(
                "Trial must be outside the construction repository and ancestors"
            )
        if out.exists() and (not out.is_dir() or any(out.iterdir())):
            raise ValueError("Refusing nonempty trial destination")
        shutil.copytree(
            EXPERIMENTS / "starter",
            out,
            dirs_exist_ok=True,
            ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"),
        )
        if args.arm != "A":
            shutil.copytree(
                EXPERIMENTS / "overlays" / args.arm, out, dirs_exist_ok=True
            )
        common = frozen["starter"]
        actual = manifest(out)
        if any(actual.get(name) != value for name, value in common.items()):
            raise ValueError("Common-file hashes differ")
        metadata = {
            "arm": args.arm,
            "common": common,
            "additions": {k: v for k, v in actual.items() if k not in common},
            "input_hash": digest(actual),
            "isolation": "not established; inspect effective guidance before launch",
        }
        (out / "trial-input-manifest.json").write_text(
            json.dumps(metadata, indent=2) + "\n"
        )
        print(f"Prepared {args.arm}: {out}; no session launched")
        return 0
    except (ValueError, OSError) as error:
        parser.exit(2, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
