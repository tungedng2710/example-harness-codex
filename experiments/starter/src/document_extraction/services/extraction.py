"""Extraction use case, independent of the HTTP framework."""

from document_extraction.inference.rules import extract
from document_extraction.schemas.contracts import ExtractResponse


def extract_document(text: str) -> ExtractResponse:
    return ExtractResponse(fields=extract(text))
