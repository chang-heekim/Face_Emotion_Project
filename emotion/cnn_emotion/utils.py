from torchvision import transforms


def image_to_tensor(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.Grayscale(1),
        transforms.ToTensor(),
        transforms.Normalize(0.5, 0.5),
    ])
    return transform(image)
