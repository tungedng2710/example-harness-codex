"""HTTP contracts and framework-neutral field values."""

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StrictStr,
    field_validator,
)


class ExtractRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: StrictStr = Field(min_length=1, max_length=10_000)

    include_confidence: StrictBool = False

    @field_validator("text")
    @classmethod
    def nonblank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must contain non-whitespace characters")
        return value


class Fields(BaseModel):
    invoice_number: str | None = None
    date: str | None = None
    total: str | None = None
    currency: str | None = None


class Confidence(BaseModel):
    invoice_number: float
    date: float
    total: float
    currency: float


class ExtractResponse(BaseModel):
    fields: Fields
    confidence: Confidence | None = None
