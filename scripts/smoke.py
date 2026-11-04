"""Offline in-process smoke check; no running server required."""

from fastapi.testclient import TestClient

from document_extraction.main import app

with TestClient(app) as client:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    response = client.post(
        "/extract",
        json={
            "text": "Invoice Number: INV-001\n"
            "Date: 2026-01-15\nTotal: 123.45\nCurrency: usd"
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "fields": {
            "invoice_number": "INV-001",
            "date": "2026-01-15",
            "total": "123.45",
            "currency": "USD",
        }
    }
print("Smoke: pass")
