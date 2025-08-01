import torch
import torch.nn as nn


# define the CNN architecture
class MyModel(nn.Module):
    def __init__(self, num_classes: int = 1000, dropout: float = 0.7) -> None:

        super().__init__()

        # YOUR CODE HERE
        # Define a CNN architecture. Remember to use the variable num_classes
        # to size appropriately the output of your classifier, and if you use
        # the Dropout layer, use the variable "dropout" to indicate how much
        # to use (like nn.Dropout(p=dropout))
        
        hidden1 = 1024
        hidden2 = 512
        
        self.model = nn.Sequential(
        
            # Conolutional Layer 1
            nn.Conv2d(3, 16, 3, padding = 1) # 224 input
            , nn.ReLU()
            , nn.MaxPool2d(2, 2)
            , nn.BatchNorm2d(16)

            # Conolutional Layer 2
            , nn.Conv2d(16, 32, 3, padding = 1)# 112 input
            , nn.ReLU()
            , nn.MaxPool2d(2, 2)
            , nn.BatchNorm2d(32)

            # Conolutional Layer 3
            , nn.Conv2d(32, 64, 3, padding = 1)# 56 input
            , nn.ReLU()
            , nn.MaxPool2d(2, 2)
            , nn.BatchNorm2d(64)

            # Conolutional Layer 4
            , nn.Conv2d(64, 128, 3, padding = 1)# 28 input, 28 Output
            , nn.ReLU()
            , nn.MaxPool2d(2, 2)
            , nn.BatchNorm2d(128)
            
            # Flatten input for MLP
            , nn.Flatten()
            
            # Linear layers of MLP
            , nn.Linear(14*14*128, hidden1) #14*14*128 input
            , nn.ReLU()
            , nn.BatchNorm1d(hidden1)
            , nn.Dropout(p = dropout)
            
            , nn.Linear(hidden1, hidden2)
            , nn.ReLU()
            , nn.BatchNorm1d(hidden2)
            , nn.Dropout(p = dropout)
            
            , nn.Linear(hidden2, num_classes)       
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # YOUR CODE HERE: process the input tensor through the
        # feature extractor, the pooling and the final linear
        # layers (if appropriate for the architecture chosen)
        
        x = self.model(x)
        
        return x


######################################################################################
#                                     TESTS
######################################################################################
import pytest


@pytest.fixture(scope="session")
def data_loaders():
    from .data import get_data_loaders

    return get_data_loaders(batch_size=2)


def test_model_construction(data_loaders):

    model = MyModel(num_classes=23, dropout=0.3)

    dataiter = iter(data_loaders["train"])
    images, labels = dataiter.next()

    out = model(images)

    assert isinstance(
        out, torch.Tensor
    ), "The output of the .forward method should be a Tensor of size ([batch_size], [n_classes])"

    assert out.shape == torch.Size(
        [2, 23]
    ), f"Expected an output tensor of size (2, 23), got {out.shape}"
