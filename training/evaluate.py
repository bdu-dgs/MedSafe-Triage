import json

import numpy as np
import torch
from torch.utils.data import DataLoader

from app.core.config import get_settings
from app.model.loader import load_checkpoint
from app.services.calibration import fit_temperature, save_calibration
from training.common import make_dataset
from training.metrics import binary_metrics


def collect(model, loader, device):
    logits, labels = [], []
    with torch.no_grad():
        for images, batch_labels in loader:
            logits.extend(model(images.to(device)).view(-1).cpu().numpy())
            labels.extend(batch_labels.view(-1).numpy())
    return np.asarray(logits), np.asarray(labels).astype(int)


def run():
    settings = get_settings(); device = torch.device(settings.device_name)
    settings.configure_runtime()
    if not settings.checkpoint_path.exists():
        raise FileNotFoundError(f"Missing checkpoint: {settings.checkpoint_path}. Run training first.")
    model, _ = load_checkpoint(settings.checkpoint_path, device)
    val_loader = DataLoader(make_dataset(settings, "val"), batch_size=settings.batch_size, shuffle=False)
    test_loader = DataLoader(make_dataset(settings, "test"), batch_size=settings.batch_size, shuffle=False)
    val_logits, val_labels = collect(model, val_loader, device)
    temperature = fit_temperature(val_logits, val_labels)
    save_calibration(settings.calibration_path, temperature)
    test_logits, test_labels = collect(model, test_loader, device)
    raw = binary_metrics(test_labels, 1 / (1 + np.exp(-test_logits)))
    calibrated = binary_metrics(test_labels, 1 / (1 + np.exp(-test_logits / temperature)))
    output = {"temperature": temperature, "raw": raw, "calibrated": calibrated}
    (settings.artifact_dir / "metrics.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    run()
