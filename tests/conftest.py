import pytest
import torch
import torch.nn as nn
import torch.optim as optim
from sacred import Experiment
from torchvision import (
    datasets,
    transforms,
)


@pytest.fixture(scope="session")
def model() -> nn.Module:
    class BaseModel(nn.Module):
        def __init__(self, input_sz=32 * 32 * 3, n_classes=10):
            super(BaseModel, self).__init__()
            self.lin = nn.Linear(input_sz, n_classes)

        def forward(self, in_tensor):
            x = in_tensor.view(-1, 32 * 32 * 3)
            return self.lin(x)

    return BaseModel()


@pytest.fixture(scope="session")
def experiment(model) -> Experiment:
    ex = Experiment("image_classification", interactive=True)

    # Log hyperparameters
    @ex.config
    def cfg():
        data_dir = "data/CIFAR10"  # noqa: F841
        data_tfms = {  # noqa: F841
            "train": transforms.Compose(
                [
                    transforms.RandomHorizontalFlip(),
                    transforms.ToTensor(),
                    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
                ]
            )
        }
        lr = 1e-2  # noqa: F841
        bs = 128  # noqa: F841
        n_classes = 10  # noqa: F841
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")  # noqa: F841

    # Log loss and metrics
    @ex.main
    def run(data_dir, data_tfms, lr, bs, device, _run):
        train_set = datasets.CIFAR10(data_dir, transform=data_tfms["train"], download=True)
        train_loader = torch.utils.data.DataLoader(train_set, batch_size=bs, shuffle=True, num_workers=2)
        model.to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=lr)

        for i, (x, y) in enumerate(train_loader, 0):
            x, y = x.to(device), y.to(device)
            optimizer.zero_grad()
            outputs = model.forward(x)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, y)
            acc = (torch.sum(preds == y.data)) / len(x)

            # Log loss
            ex.log_scalar("training/batch/loss", loss)
            # Log accuracy
            ex.log_scalar("training/batch/acc", acc)

            loss.backward()
            optimizer.step()

        return {"final_loss": loss.item(), "final_acc": acc.cpu().item()}

    return ex
