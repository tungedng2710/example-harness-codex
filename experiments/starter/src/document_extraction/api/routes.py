"""Validate, delegate and serialize; no extraction rules here."""

from fastapi import APIRouter

from document_extraction.schemas.contracts import ExtractRequest, ExtractResponse
from document_extraction.services.extraction import extract_document

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/extract", response_model=ExtractResponse)
def extraction(request: ExtractRequest) -> ExtractResponse:
    return extract_document(request.text)
