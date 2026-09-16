from pathlib import Path

import numpy as np
import torch
from PIL import Image
import matplotlib.cm as cm


class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.activations = None
        self.gradients = None
        target_layer.register_forward_hook(self._save_activations)
        target_layer.register_full_backward_hook(self._save_gradients)

    def _save_activations(self, _, __, output):
        self.activations = output

    def _save_gradients(self, _, __, grad_output):
        self.gradients = grad_output[0]

    def generate(self, tensor: torch.Tensor, class_index: int, original: Image.Image, output_path: Path) -> None:
        self.model.zero_grad(set_to_none=True)
        logits = self.model(tensor)
        score = logits[:, 0] if class_index == 1 else -logits[:, 0]
        score.sum().backward()
        weights = self.gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * self.activations).sum(dim=1).relu()[0]
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        cam_img = Image.fromarray((cam.detach().cpu().numpy() * 255).astype(np.uint8)).resize(original.size)
        heat = (cm.get_cmap("jet")(np.asarray(cam_img) / 255.0)[:, :, :3] * 255).astype(np.uint8)
        base = np.asarray(original.convert("RGB")).astype(np.float32)
        overlay = (0.55 * base + 0.45 * heat).clip(0, 255).astype(np.uint8)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(overlay).save(output_path)

