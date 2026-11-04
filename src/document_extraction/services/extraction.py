"""Extraction use case, independent of the HTTP framework."""

from document_extraction.inference.rules import extract
from document_extraction.schemas.contracts import Confidence, ExtractResponse


def extract_document(text: str, include_confidence: bool = False) -> ExtractResponse:
    fields = extract(text)
    if include_confidence:
        scores = {
            key: 1.0 if value is not None else 0.0
            for key, value in fields.model_dump().items()
        }
        return ExtractResponse(fields=fields, confidence=Confidence(**scores))
    return ExtractResponse(fields=fields)
