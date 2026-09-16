import random
from pathlib import Path

import numpy as np
import torch
from medmnist import PneumoniaMNIST

from app.core.config import Settings
from app.services.preprocessing import build_transform


def seed_everything(seed: int):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def make_dataset(settings: Settings, split: str, train: bool = False):
    # MedMNIST expects the root directory to exist before it initializes its
    # download/cache layout. Resolve relative paths from the repository root so
    # the training and serving commands behave consistently from any cwd.
    data_dir = settings.data_dir
    if not data_dir.is_absolute():
        data_dir = Path.cwd() / data_dir
    data_dir.mkdir(parents=True, exist_ok=True)
    try:
        return PneumoniaMNIST(
            root=str(data_dir.resolve()),
            split=split,
            download=True,
            transform=build_transform(settings, train=train),
        )
    except RuntimeError as exc:
        if "Automatic download failed" in str(exc):
            raise RuntimeError(
                f"PneumoniaMNIST could not be downloaded into {data_dir.resolve()}. "
                "Check network access to Zenodo and retry; the data directory itself is ready."
            ) from exc
        raise
