from dataclasses import dataclass
from pathlib import Path
import uuid

import torch
from PIL import Image

from app.core.config import Settings
from app.services.calibration import load_temperature
from app.services.gradcam import GradCAM
from app.services.preprocessing import preprocess_image


CLASS_NAMES = {0: "Normal", 1: "Pneumonia"}


@dataclass
class Prediction:
    predicted_class: str
    confidence: float
    probabilities: dict[str, float]
    needs_review: bool
    review_reason: str | None
    gradcam_path: Path


class InferenceService:
    def __init__(self, model, settings: Settings, device: torch.device):
        self.model = model
        self.settings = settings
        self.device = device
        self.temperature = load_temperature(settings.calibration_path) if settings.use_calibration else 1.0
        self.gradcam = GradCAM(model, model.layer4[-1].conv2)

    @torch.inference_mode(False)
    def predict(self, image: Image.Image) -> Prediction:
        tensor = preprocess_image(image, self.settings).to(self.device)
        self.model.zero_grad(set_to_none=True)
        logits = self.model(tensor)[:, 0] / self.temperature
        probability = float(torch.sigmoid(logits).item())
        class_index = int(probability >= 0.5)
        probabilities = {"Normal": 1.0 - probability, "Pneumonia": probability}
        confidence = probabilities[CLASS_NAMES[class_index]]
        needs_review = confidence < self.settings.review_confidence_threshold
        output_path = self.settings.artifact_dir / "gradcam" / f"{uuid.uuid4().hex}.png"
        self.gradcam.generate(tensor, class_index, image, output_path)
        return Prediction(CLASS_NAMES[class_index], confidence, probabilities, needs_review,
                          "Prediction confidence below configured review threshold" if needs_review else None,
                          output_path)

