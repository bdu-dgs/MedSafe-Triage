# MedSafe Triage architecture

## Problem

MedSafe Triage is a small, reproducible demonstration of serving a binary chest-X-ray classifier. It trains on the official PneumoniaMNIST train/validation/test splits, exposes inference through FastAPI, and routes uncertain predictions toward human review.

## System map

```text
PneumoniaMNIST
  → shared preprocessing (grayscale → RGB, resize, ImageNet normalization)
  → pretrained ResNet18 fine-tuning
  → validation checkpoint + temperature calibration
  → FastAPI startup model load
  → prediction + review decision + Grad-CAM artifact
  → static browser demo
```

## Responsibilities and interfaces

- `training/common.py`: dataset construction and reproducibility helpers.
- `app/services/preprocessing.py`: the image transform contract used by training and serving.
- `app/model/network.py`: ResNet18 construction and binary output head.
- `training/train.py`: optimization, validation, and checkpoint writing.
- `training/evaluate.py`: held-out evaluation and validation-only temperature fitting.
- `app/services/inference.py`: model-facing prediction service and review policy.
- `app/services/gradcam.py`: interpretation visualization, explicitly not causal explanation.
- `app/api/routes.py`: upload validation, HTTP mapping, and response schema.
- `frontend/index.html`: minimal user-facing workflow.

## Artifact contract

`artifacts/best_model.pt` contains `model_state_dict`, model metadata, and best validation F1. `artifacts/calibration.json` contains the fitted temperature. These artifacts are created by training/evaluation and consumed by the service. If a checkpoint is absent, the API can start with ImageNet weights for a demo, but real project predictions require a trained checkpoint.

## Design decisions

### 1. Pretrained ResNet18

**Decision:** fine-tune torchvision ResNet18 and replace its final layer with one binary logit.

**Why / benefits:** transfer learning gives a fast, credible MVP on a small image dataset and uses a well-tested implementation.

**Costs:** ImageNet priors may not be optimal for radiographs, and the weight download adds setup dependency. Training from scratch becomes more appropriate with substantially more domain data or a domain-pretrained backbone.

### 2. Grayscale to RGB

**Decision:** replicate the grayscale channel into three channels through `Grayscale(num_output_channels=3)`.

**Why / benefits:** preserves the pretrained first convolution and keeps the checkpoint compatible with standard ResNet18 weights.

**Costs:** three channels contain duplicated information. Modifying `conv1` is more domain-specific, but it sacrifices direct compatibility and creates another initialization decision.

### 3. FastAPI plus a static frontend

**Decision:** put HTTP concerns in FastAPI and serve a lightweight HTML/JavaScript client.

**Why / benefits:** a stable JSON contract makes the model reusable while avoiding a frontend build system for a single workflow.

**Costs:** production deployment still needs authentication, observability, and resource controls. React becomes more useful when the UI has several views, shared state, or a larger team.

### 4. Startup model loading

**Decision:** load the model once during application lifespan.

**Why / benefits:** inference requests reuse weights and hooks, avoiding repeated disk access and initialization latency.

**Costs:** process memory holds the model and a bad artifact prevents a clean startup. A worker pool or model server becomes more appropriate at higher traffic or when multiple models are served.

### 5. Confidence-based review

**Decision:** mark predictions below one centralized threshold as `needs_review`.

**Why / benefits:** makes uncertainty actionable and demonstrates a human-in-the-loop boundary.

**Costs:** the threshold is a demonstration, not clinically validated triage. A real workflow would select operating points with domain experts, subgroup analysis, prospective validation, and explicit alert costs.

## Validation boundaries

Implemented: unit tests for preprocessing, response-adjacent logic, health, invalid uploads; train/evaluate commands; artifact-backed inference; API/frontend integration path.

Not established by this repository alone: clinical utility, causal explanation, deployment availability, regulatory compliance, or performance on populations outside the dataset.

