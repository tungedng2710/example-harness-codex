import pytest

from document_extraction.inference.rules import extract, validate


@pytest.mark.parametrize(
    "key,value,expected",
    [
        ("date", "2024-02-29", "2024-02-29"),
        ("date", "2025-02-29", None),
        ("date", "2026-13-01", None),
        ("date", "２０２６-01-01", None),
        ("total", "0", "0.00"),
        ("total", "0001.2", "1.20"),
        ("total", "9" * 100, "9" * 100 + ".00"),
        *[
            ("total", value, None)
            for value in [
                "-1",
                "+1",
                "1e2",
                "1,000",
                ".5",
                "1.",
                "1.234",
                "１２",
                "NaN",
            ]
        ],
        ("currency", "usd", "USD"),
        ("currency", "üsd", None),
        ("currency", "US", None),
        ("invoice_number", "a-12", "a-12"),
        ("invoice_number", "a" * 41, None),
        ("invoice_number", "INV_1", None),
    ],
)
def test_validation(key, value, expected):
    assert validate(key, value) == expected


def test_labels_duplicates():
    result = extract(
        "  iNvOiCe NuMbEr : bad!\n"
        "Invoice Number: ok-1\nInvoice Number: later\n"
        "prefix Total: 9\n Total : 1.2 \nCurrency: KSD\nCurrency: usd"
    )
    assert result.model_dump() == {
        "invoice_number": "ok-1",
        "date": None,
        "total": "1.20",
        "currency": "USD",
    }
