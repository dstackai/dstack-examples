import os
from pathlib import Path
from typing import Optional

import hydra
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchmetrics import Accuracy
from torchvision import transforms
from torchvision.datasets import MNIST

DIR = Path(__file__).parent.parent


def get_ckpt_path(cfg) -> Optional[Path]:
    """Get the ckpt_path for resuming training from the last of lightning_logs/version_x if requested and available"""
    ckpt_path = None  # default
    if not cfg.get('resume'):  # don't resume
        return ckpt_path

    # first, try .pl_auto_save.ckpt from PL_FAULT_TOLERANT_TRAINING
    if (path := DIR / '.pl_auto_save.ckpt').exists():
        ckpt_path = path
    # next, find the latest lightning_logs/version_*/checkpoints/*.ckpt by creation time
    elif (default_dir := DIR / 'lightning_logs').exists():
        ckpts = list(default_dir.glob('version_*/checkpoints/*.ckpt'))
        if ckpts and (latest_ckpt := max(ckpts, key=lambda x: x.stat().st_ctime)):
            ckpt_path = latest_ckpt

    if ckpt_path is not None:
        print(f'Resuming training from checkpoint: {ckpt_path}')
    return ckpt_path


class MNISTDataModule(pl.LightningDataModule):
    # Datamodule adapted from https://pytorch-lightning.readthedocs.io/en/stable/extensions/datamodules.html#what-is-a-datamodule
    def __init__(self, data_dir: str = DIR / 'data', batch_size: int = 32, num_workers: int = os.cpu_count(),
                 download: bool = True):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])
        self.download = download

    def prepare_data(self):
        # download
        MNIST(self.data_dir, train=True, download=self.download)
        MNIST(self.data_dir, train=False, download=self.download)

    def setup(self, stage: Optional[str] = None):
        # Assign train/val datasets for use in dataloaders
        if stage == 'fit' or stage is None:
            mnist_full = MNIST(self.data_dir, train=True, transform=self.transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        # Assign test dataset for use in dataloader(s)
        if stage == 'test' or stage is None:
            self.mnist_test = MNIST(self.data_dir, train=False, transform=self.transform)

        if stage == 'predict' or stage is None:
            self.mnist_predict = MNIST(self.data_dir, train=False, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=self.batch_size, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.batch_size, num_workers=self.num_workers)

    def predict_dataloader(self):
        return DataLoader(self.mnist_predict, batch_size=self.batch_size)


class LitMNIST(pl.LightningModule):
    # example adapted from https://pytorch-lightning.readthedocs.io/en/stable/notebooks/lightning_examples/mnist-hello-world.html#A-more-complete-MNIST-Lightning-Module-Example
    def __init__(self, hidden_size=64, learning_rate=2e-4):
        super().__init__()
        # Set our init args as class attributes
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate

        # Hardcode some dataset specific attributes
        self.num_classes = 10
        channels, width, height = (1, 28, 28)

        # Define PyTorch model
        self.model = nn.Sequential(
            nn.Flatten(),
            nn.Linear(channels * width * height, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.1),
            nn.Linear(hidden_size, self.num_classes),
        )

        self.accuracy = Accuracy()

    def forward(self, x):
        return self.model(x)

    def training_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        return loss

    def validation_step(self, batch, batch_idx):
        x, y = batch
        logits = self(x)
        loss = F.cross_entropy(logits, y)
        preds = torch.argmax(logits, dim=1)
        self.accuracy(preds, y)

        # Calling self.log will surface up scalars for you in TensorBoard
        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', self.accuracy, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx):
        # Here we just reuse the validation_step for testing
        return self.validation_step(batch, batch_idx)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer


@hydra.main(version_base=None, config_path=str(DIR), config_name='config')
def main(cfg):
    dm = MNISTDataModule(**cfg.datamodule)
    model = LitMNIST(**cfg.model)

    trainer = pl.Trainer(**cfg.trainer)
    trainer.fit(model, datamodule=dm, ckpt_path=str(p) if (p := get_ckpt_path(cfg)) else None)
    trainer.test(datamodule=dm, ckpt_path='best')


if __name__ == '__main__':
    main()
