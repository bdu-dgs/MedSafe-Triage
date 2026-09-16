from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    predicted_class: str
    confidence: float = Field(ge=0, le=1)
    probabilities: dict[str, float]
    needs_review: bool
    review_reason: str | None = None
    gradcam_url: str


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str

