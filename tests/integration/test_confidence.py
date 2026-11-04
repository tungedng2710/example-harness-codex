import pytest
from fastapi.testclient import TestClient

from document_extraction.main import app

client = TestClient(app)


@pytest.mark.parametrize("flag", [None, False, True])
def test_optional_shape(flag):
    body = {"text": "Total: 4.5"}
    if flag is not None:
        body["include_confidence"] = flag
    response = client.post("/extract", json=body)
    assert response.status_code == 200
    fields = {"invoice_number": None, "date": None, "total": "4.50", "currency": None}
    expected = {"fields": fields}
    if flag:
        expected["confidence"] = {
            "invoice_number": 0.0,
            "date": 0.0,
            "total": 1.0,
            "currency": 0.0,
        }
    assert response.json() == expected


@pytest.mark.parametrize("flag", [0, 1, "true", "false", None, [], {}, 0.0])
def test_strict_flag(flag):
    assert (
        client.post(
            "/extract", json={"text": "x", "include_confidence": flag}
        ).status_code
        == 422
    )


def test_document_not_logged_at_debug(caplog, capsys):
    caplog.set_level("DEBUG")
    marker = "synthetic-document-marker-do-not-log-5821"
    response = client.post(
        "/extract", json={"text": marker, "include_confidence": True}
    )
    assert response.status_code == 200
    assert marker not in caplog.text
    captured = capsys.readouterr()
    assert marker not in captured.out + captured.err
