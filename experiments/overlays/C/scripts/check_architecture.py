"""Check static import edges under one selected source package."""

import argparse
import ast
from pathlib import Path

FORBIDDEN = {
    "services": ("fastapi", "starlette", "document_extraction.api"),
    "inference": (
        "fastapi",
        "starlette",
        "document_extraction.api",
        "document_extraction.services",
    ),
    "schemas": (
        "document_extraction.api",
        "document_extraction.services",
        "document_extraction.inference",
    ),
}


def violations(root: Path) -> list[str]:
    findings = []
    for path in sorted(root.rglob("*.py")):
        relative = path.relative_to(root)
        layer = relative.parts[0]
        package = ["document_extraction", *relative.parts[:-1]]
        for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                base = node.module or ""
                if node.level:
                    base = ".".join(
                        package[: len(package) - node.level + 1]
                        + ([base] if base else [])
                    )
                names = [base, *[f"{base}.{alias.name}" for alias in node.names]]
            for name in names:
                if any(
                    name == banned or name.startswith(banned + ".")
                    for banned in FORBIDDEN.get(layer, ())
                ):
                    findings.append(f"{path}:{node.lineno}: {layer} forbids {name}")
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("src/document_extraction"))
    args = parser.parse_args()
    if not args.source.is_dir():
        parser.error("source package directory does not exist")
    findings = violations(args.source)
    print("\n".join(findings) if findings else "Architecture imports: pass")
    return bool(findings)


if __name__ == "__main__":
    raise SystemExit(main())
