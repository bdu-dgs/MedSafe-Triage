from PIL import Image
import torch
from torchvision import transforms

from app.core.config import Settings


def build_transform(settings: Settings, train: bool = False):
    operations = [transforms.Grayscale(num_output_channels=3)]
    if train:
        operations += [transforms.Resize((settings.image_size, settings.image_size)), transforms.RandomHorizontalFlip()]
    else:
        operations += [transforms.Resize((settings.image_size, settings.image_size))]
    operations += [
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
    return transforms.Compose(operations)


def preprocess_image(image: Image.Image, settings: Settings) -> torch.Tensor:
    return build_transform(settings)(image.convert("L")).unsqueeze(0)

