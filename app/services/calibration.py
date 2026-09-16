import json
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn


def fit_temperature(logits: np.ndarray, labels: np.ndarray) -> float:
    logit_tensor = torch.tensor(logits, dtype=torch.float32)
    label_tensor = torch.tensor(labels, dtype=torch.float32)
    temperature = nn.Parameter(torch.ones(1))
    optimizer = torch.optim.LBFGS([temperature], lr=0.05, max_iter=50)

    def closure():
        optimizer.zero_grad()
        loss = nn.functional.binary_cross_entropy_with_logits(logit_tensor / temperature.clamp_min(0.05), label_tensor)
        loss.backward()
        return loss

    optimizer.step(closure)
    return float(temperature.detach().clamp_min(0.05).item())


def save_calibration(path: Path, temperature: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"temperature": temperature}, indent=2), encoding="utf-8")


def load_temperature(path: Path) -> float:
    if not path.exists():
        return 1.0
    return float(json.loads(path.read_text(encoding="utf-8")).get("temperature", 1.0))

