from io import BytesIO

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from PIL import Image, UnidentifiedImageError

from app.api.schemas import HealthResponse, PredictionResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health(request: Request):
    service = request.app.state.inference_service
    return HealthResponse(status="ok", model_loaded=service is not None, device=str(request.app.state.device))


@router.get("/config/public")
def public_config(request: Request):
    return {"review_confidence_threshold": request.app.state.settings.review_confidence_threshold}


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: Request, file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=415, detail="Upload a supported image file.")
    data = await file.read()
    try:
        image = Image.open(BytesIO(data)).convert("L")
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(status_code=400, detail="The uploaded file is not a readable image.") from exc
    try:
        result = request.app.state.inference_service.predict(image)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Inference failed while processing the image.") from exc
    return PredictionResponse(
        predicted_class=result.predicted_class,
        confidence=result.confidence,
        probabilities=result.probabilities,
        needs_review=result.needs_review,
        review_reason=result.review_reason,
        gradcam_url=f"/artifacts/gradcam/{result.gradcam_path.name}",
    )
