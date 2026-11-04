"""Pure rules; document content is data, never instructions."""

import re
from datetime import date
from decimal import Decimal, localcontext

from document_extraction.schemas.contracts import Fields

LABEL = re.compile(r"^\s*(Invoice Number|Date|Total|Currency)\s*:\s*(.*?)\s*$", re.I)
KEYS = {
    "invoice number": "invoice_number",
    "date": "date",
    "total": "total",
    "currency": "currency",
}


def validate(key: str, value: str) -> str | None:
    if key == "invoice_number":
        return value if re.fullmatch(r"[A-Za-z0-9-]{1,40}", value) else None
    if key == "date":
        if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            return None
        try:
            date.fromisoformat(value)
        except ValueError:
            return None
        return value
    if key == "total":
        if not re.fullmatch(r"[0-9]+(?:\.[0-9]{1,2})?", value):
            return None
        with localcontext() as context:
            context.prec = max(28, len(value) + 2)
            return format(Decimal(value).quantize(Decimal("0.01")), "f")
    if key == "currency" and re.fullmatch(r"[A-Za-z]{3}", value):
        return value.upper()
    return None


def extract(text: str) -> Fields:
    values: dict[str, str | None] = dict.fromkeys(KEYS.values())
    for line in text.splitlines():
        match = LABEL.fullmatch(line)
        if match:
            key = KEYS[match[1].lower()]
            if values[key] is None:
                values[key] = validate(key, match[2].strip())
    return Fields(**values)
