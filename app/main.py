from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import get_settings
from app.model.loader import load_checkpoint
from app.model.network import build_model
from app.services.inference import InferenceService


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    settings.configure_runtime()
    settings.artifact_dir.mkdir(parents=True, exist_ok=True)
    device = torch.device(settings.device_name)
    if settings.checkpoint_path.exists():
        model, _ = load_checkpoint(settings.checkpoint_path, device)
    else:
        model = build_model(pretrained=True).to(device).eval()
    app.state.settings = settings
    app.state.device = device
    app.state.inference_service = InferenceService(model, settings, device)
    yield


app = FastAPI(title="MedSafe Triage", description="PneumoniaMNIST model-serving demo", lifespan=lifespan)
app.include_router(router)
app.mount("/artifacts", StaticFiles(directory="artifacts", check_dir=False), name="artifacts")
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
