# MedSafe Triage

An end-to-end portfolio project for a confidence-aware PneumoniaMNIST classifier: PyTorch/ResNet18 training, calibration, Grad-CAM visualization, FastAPI inference, and a minimal browser demo.

## Architecture

```text
PneumoniaMNIST → shared preprocessing → ResNet18 → validation checkpoint
                                      → calibration → FastAPI → browser demo
                                                     ↘ Grad-CAM + review state
```

See [docs/architecture.md](docs/architecture.md) for boundaries and trade-offs.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

The official MedMNIST package downloads PneumoniaMNIST automatically. torchvision downloads pretrained ResNet18 weights automatically. The first run therefore needs network access and disk space.

## Train and evaluate

```powershell
python -m training.train
python -m training.evaluate
```

The default configuration is an intentionally fast MVP (`2` epochs, CPU/GPU auto-detection). Override settings with `MEDSAFE_` environment variables, for example `MEDSAFE_EPOCHS=10` or `MEDSAFE_REVIEW_CONFIDENCE_THRESHOLD=0.8`.

Evaluation writes raw and temperature-calibrated accuracy, precision, sensitivity/recall, specificity, F1, AUROC, confusion matrix, Brier score, and ECE to `artifacts/metrics.json`. Metrics are never fabricated.

The current verified smoke run used `MEDSAFE_EPOCHS=1`, `MEDSAFE_IMAGE_SIZE=64`, and `MEDSAFE_BATCH_SIZE=64` on CPU. Its calibrated test metrics are: accuracy `0.7869`, sensitivity `0.9872`, specificity `0.4530`, F1 `0.8527`, AUROC `0.9264`, Brier `0.1645`, and ECE `0.1781`. These are engineering-demo results, not clinical performance claims.

## Run the demo

```powershell
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000. `GET /health` reports service health. `POST /predict` accepts a multipart image upload and returns:

```json
{
  "predicted_class": "Pneumonia",
  "confidence": 0.87,
  "probabilities": {"Normal": 0.13, "Pneumonia": 0.87},
  "needs_review": false,
  "review_reason": null,
  "gradcam_url": "/artifacts/<generated-file>.png"
}
```

The threshold is a human-review demonstration, not a clinical decision threshold. Grad-CAM is an interpretation visualization and does not prove causal medical reasoning.

## Tests

```powershell
pytest
```

## Implemented vs future work

Implemented: reproducible dataset download, transfer-learning training, validation checkpointing, held-out evaluation, temperature scaling, shared preprocessing, startup model loading, FastAPI health/predict endpoints, upload validation, review state, Grad-CAM, and responsive static UI.

Possible future work: clinical threshold selection, subgroup and external validation, authentication, rate limits, audit logging, model registry/versioning, background jobs for large images, richer monitoring, and deployment hardening.
