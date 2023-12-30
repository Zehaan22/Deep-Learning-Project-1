"""File to test out approaches to the code."""

import torch
from torch import nn


class DigitModel(nn.Module):
    """This is the multiclass classification model for matrix to digits."""

    def __init__(self, in_features=900):
        """Create an instance of the model."""
        super().__init__()
        self.linear_stack = nn.Sequential(
            nn.Linear(
                in_features=in_features,
                out_features=16
            ),
            nn.ReLU(),
            nn.Linear(
                in_features=16,
                out_features=32
            ),
            nn.ReLU(),
            nn.Linear(
                in_features=32,
                out_features=16
            ),
            nn.ReLU(),
            nn.Linear(
                in_features=16,
                out_features=10
            )
        )

    def forward(self, x):
        return self.linear_stack(x)

    def logits_to_preds(self, logits):
        """Convert Logits to predictions."""
        probs = torch.softmax(logits,
                              dim=1)
        preds = torch.argmax(probs,
                             dim=1)
        return preds
