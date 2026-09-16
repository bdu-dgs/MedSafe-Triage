import numpy as np
from sklearn.metrics import (accuracy_score, brier_score_loss, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score)


def expected_calibration_error(probabilities, labels, bins: int = 10) -> float:
    probabilities, labels = np.asarray(probabilities), np.asarray(labels)
    edges = np.linspace(0, 1, bins + 1)
    ece = 0.0
    for low, high in zip(edges[:-1], edges[1:]):
        mask = (probabilities > low) & (probabilities <= high)
        if mask.any():
            ece += mask.mean() * abs(probabilities[mask].mean() - labels[mask].mean())
    return float(ece)


def binary_metrics(labels, probabilities):
    labels, probabilities = np.asarray(labels).astype(int), np.asarray(probabilities)
    predictions = (probabilities >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(labels, predictions, labels=[0, 1]).ravel()
    return {
        "accuracy": float(accuracy_score(labels, predictions)),
        "precision": float(precision_score(labels, predictions, zero_division=0)),
        "recall_sensitivity": float(recall_score(labels, predictions, zero_division=0)),
        "specificity": float(tn / (tn + fp)) if tn + fp else 0.0,
        "f1": float(f1_score(labels, predictions, zero_division=0)),
        "auroc": float(roc_auc_score(labels, probabilities)) if len(np.unique(labels)) > 1 else None,
        "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
        "brier_score": float(brier_score_loss(labels, probabilities)),
        "ece": expected_calibration_error(probabilities, labels),
    }

