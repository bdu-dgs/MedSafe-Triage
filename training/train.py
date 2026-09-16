import json
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from app.core.config import get_settings
from app.model.network import build_model
from training.common import make_dataset, seed_everything


def run():
    settings = get_settings()
    settings.configure_runtime()
    seed_everything(settings.random_seed)
    device = torch.device(settings.device_name)
    train_ds = make_dataset(settings, "train", train=True)
    val_ds = make_dataset(settings, "val")
    train_loader = DataLoader(train_ds, batch_size=settings.batch_size, shuffle=True, num_workers=settings.num_workers)
    val_loader = DataLoader(val_ds, batch_size=settings.batch_size, shuffle=False, num_workers=settings.num_workers)
    model = build_model(pretrained=True).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=settings.learning_rate)
    criterion = torch.nn.BCEWithLogitsLoss()
    best_f1 = -1.0
    history = []
    settings.artifact_dir.mkdir(parents=True, exist_ok=True)
    for epoch in range(settings.epochs):
        model.train()
        running_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.float().to(device).view(-1)
            optimizer.zero_grad(set_to_none=True)
            loss = criterion(model(images).view(-1), labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * len(images)
        val_loss, val_f1 = validate(model, val_loader, criterion, device)
        row = {"epoch": epoch + 1, "train_loss": running_loss / len(train_ds), "val_loss": val_loss, "val_f1": val_f1}
        history.append(row)
        print(f"epoch={epoch + 1} train_loss={row['train_loss']:.4f} val_loss={val_loss:.4f} val_f1={val_f1:.4f}")
        if val_f1 > best_f1:
            best_f1 = val_f1
            torch.save({"model_state_dict": model.state_dict(), "settings": {"image_size": settings.image_size, "model_name": settings.model_name}, "best_val_f1": best_f1}, settings.checkpoint_path)
    (settings.artifact_dir / "training_history.json").write_text(json.dumps(history, indent=2), encoding="utf-8")
    print(f"saved checkpoint to {settings.checkpoint_path}")


def validate(model, loader, criterion, device):
    from sklearn.metrics import f1_score
    model.eval(); total_loss = 0.0; labels_all = []; probs_all = []
    with torch.no_grad():
        for images, labels in loader:
            logits = model(images.to(device)).view(-1)
            labels = labels.float().to(device).view(-1)
            total_loss += criterion(logits, labels).item() * len(images)
            labels_all.extend(labels.cpu().numpy()); probs_all.extend(torch.sigmoid(logits).cpu().numpy())
    return total_loss / len(loader.dataset), float(f1_score(labels_all, (torch.tensor(probs_all) >= .5).numpy(), zero_division=0))


if __name__ == "__main__":
    run()
