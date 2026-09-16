from functools import lru_cache
import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


ROOT_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MEDSAFE_", env_file=".env", extra="ignore")

    model_name: str = "resnet18"
    image_size: int = 224
    batch_size: int = 32
    learning_rate: float = 1e-4
    epochs: int = 2
    random_seed: int = 42
    review_confidence_threshold: float = 0.75
    data_dir: Path = Path("data")
    artifact_dir: Path = Path("artifacts")
    checkpoint_path: Path = Path("artifacts/best_model.pt")
    calibration_path: Path = Path("artifacts/calibration.json")
    torch_cache_dir: Path = Path("artifacts/torch_cache")
    num_workers: int = 0
    use_calibration: bool = True

    @property
    def device_name(self) -> str:
        return "cuda" if __import__("torch").cuda.is_available() else "cpu"

    def configure_runtime(self) -> None:
        cache_dir = self.torch_cache_dir
        if not cache_dir.is_absolute():
            cache_dir = Path.cwd() / cache_dir
        cache_dir.mkdir(parents=True, exist_ok=True)
        os.environ.setdefault("TORCH_HOME", str(cache_dir.resolve()))


@lru_cache
def get_settings() -> Settings:
    return Settings()
