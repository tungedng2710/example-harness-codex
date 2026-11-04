import importlib.util
from pathlib import Path

import pytest

spec = importlib.util.spec_from_file_location(
    "architecture", Path(__file__).parents[2] / "scripts/check_architecture.py"
)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


@pytest.mark.parametrize(
    "layer,statement,forbidden",
    [
        ("services", "from ..inference.rules import extract", False),
        ("services", "from ..api import routes", True),
        ("services", "from .. import api", True),
        ("services", "import fastapi.routing", True),
        ("inference", "from document_extraction.services import extraction", True),
        ("schemas", "from ..inference import rules", True),
        ("schemas", "from pydantic import BaseModel", False),
        ("inference", "import decimal", False),
    ],
)
def test_edges(tmp_path, layer, statement, forbidden):
    target = tmp_path / layer / "example.py"
    target.parent.mkdir()
    target.write_text(statement)
    findings = checker.violations(tmp_path)
    assert bool(findings) is forbidden
    if forbidden:
        assert f"{target}:1:" in findings[0]
