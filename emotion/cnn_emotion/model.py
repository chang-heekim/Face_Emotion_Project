import torch
from torch import nn


class VGG(nn.Module):
    def __init__(self, base_model, n_classes):
        super(VGG, self).__init__()

        self.input_conv = nn.Conv2d(1, 3, 3, 1, 1)
        self.featrue_extractor = base_model

        self.pooling = nn.Sequential(
            nn.BatchNorm2d(512),
            nn.AdaptiveAvgPool2d(1),
            nn.Flatten()
        )
        self.cls = nn.Sequential(
            nn.Linear(512, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(256, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(32, 7),
        )

    def forward(self, input):
        x = self.input_conv(input)
        x = self.featrue_extractor(x)
        x = self.pooling(x)
        out = self.cls(x)
        return out
