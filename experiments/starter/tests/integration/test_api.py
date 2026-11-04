import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from document_extraction.main import app

client = TestClient(app)
FIXTURES = json.loads(
    (Path(__file__).parents[1] / "fixtures/invoices.json").read_text()
)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.parametrize("case", FIXTURES)
def test_fixtures_and_determinism(case, caplog):
    for _ in range(2):
        response = client.post("/extract", json={"text": case["text"]})
        assert response.status_code == 200
        assert response.json() == {"fields": case["fields"]}
    assert case["text"] not in caplog.text


@pytest.mark.parametrize(
    "body",
    [
        {},
        {"text": None},
        {"text": 1},
        {"text": True},
        {"text": []},
        {"text": ""},
        {"text": " \n\t"},
        {"text": "a", "extra": 1},
        {"text": "a" * 10001},
        {"text": " " * 10000 + "a"},
    ],
)
def test_invalid_requests(body):
    assert client.post("/extract", json=body).status_code == 422


def test_boundaries_and_malformed():
    for text in ["a" * 10000, " " * 9999 + "a", "請求書 🙂"]:
        response = client.post("/extract", json={"text": text})
        assert response.status_code == 200
        assert all(value is None for value in response.json()["fields"].values())
    assert (
        client.post(
            "/extract", content="{", headers={"Content-Type": "application/json"}
        ).status_code
        == 422
    )
