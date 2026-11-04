"""Fixed feature cases, independent of candidate public tests."""

import pytest
from fastapi.testclient import TestClient

from document_extraction.main import app

client = TestClient(app)
KEYS = ("invoice_number", "date", "total", "currency")


@pytest.mark.parametrize(
    "text,values",
    [
        (
            "Invoice Number: X-1\nDate: 2024-02-29\nTotal: 0\nCurrency: usd",
            ["X-1", "2024-02-29", "0.00", "USD"],
        ),
        ("unrecognized 🙂", [None] * 4),
        (
            "Total: invalid\nTotal: 12.3\nTotal: 77\nCurrency: eu",
            [None, None, "12.30", None],
        ),
    ],
)
def test_feature_scores(text, values):
    response = client.post("/extract", json={"text": text, "include_confidence": True})
    assert response.status_code == 200
    assert response.json() == {
        "fields": dict(zip(KEYS, values)),
        "confidence": dict(zip(KEYS, [1.0 if v is not None else 0.0 for v in values])),
    }


def test_feature_false():
    response = client.post(
        "/extract", json={"text": "unknown", "include_confidence": False}
    )
    assert response.status_code == 200
    assert response.json() == {"fields": dict.fromkeys(KEYS)}


@pytest.mark.parametrize("flag", ["true", "false", 0, 1, None, [], {}])
def test_bad_flags(flag):
    assert (
        client.post(
            "/extract", json={"text": "x", "include_confidence": flag}
        ).status_code
        == 422
    )
