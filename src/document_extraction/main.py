"""Explicit application composition root."""

from fastapi import FastAPI

from document_extraction.api.routes import router

app = FastAPI(title="Synthetic invoice extraction")
app.include_router(router)
