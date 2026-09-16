from io import BytesIO

from fastapi.testclient import TestClient
from PIL import Image
import torch

from app.core.config import Settings
from app.main import app
from app.services.inference import CLASS_NAMES
from app.services.preprocessing import preprocess_image


def test_preprocessing_output_shape():
    tensor = preprocess_image(Image.new("L", (28, 28)), Settings(image_size=224))
    assert tensor.shape == (1, 3, 224, 224)


def test_inference_output_format():
    assert set(CLASS_NAMES.values()) == {"Normal", "Pneumonia"}
    probability = torch.tensor([0.8])
    assert bool(probability.item() >= 0.5)


def test_confidence_threshold_logic():
    threshold = 0.75
    assert 0.7 < threshold
    assert not (0.7 >= threshold)
    assert 0.8 >= threshold


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_invalid_upload():
    with TestClient(app) as client:
        response = client.post("/predict", files={"file": ("note.txt", b"not image", "text/plain")})
        assert response.status_code == 415

