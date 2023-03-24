import os
from pathlib import Path
from typing import Optional

import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from pytorch_lightning.callbacks import TQDMProgressBar, EarlyStopping, ModelCheckpoint
from torch import nn
from torch.utils.data import DataLoader, random_split
from torchmetrics import Accuracy
from torchvision import transforms
from torchvision.datasets import MNIST


class MNISTDataModule(pl.LightningDataModule):
    def __init__(self, data_dir: Path = Path("data"), batch_size: int = 32, num_workers: int = os.cpu_count()):
        super().__init__()
        self.data_dir = data_dir
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])

    def prepare_data(self):
        MNIST(self.data_dir, train=True, download=True)
        MNIST(self.data_dir, train=False, download=True)

    def setup(self, stage: Optional[str] = None):
        if stage == 'fit' or stage is None:
            mnist_full = MNIST(self.data_dir, train=True, transform=self.transform)
            self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

        if stage == 'test' or stage is None:
            self.mnist_test = MNIST(self.data_dir, train=False, transform=self.transform)

    def train_dataloader(self):
        return DataLoader(self.mnist_train, batch_size=self.batch_size, num_workers=self.num_workers)

    def val_dataloader(self):
        return DataLoader(self.mnist_val, batch_size=self.batch_size, num_workers=self.num_workers)

    def test_dataloader(self):
        return DataLoader(self.mnist_test, batch_size=self.batch_size, num_workers=self.num_workers)


class LitMNIST(pl.LightningModule):
    def __init__(self, hidden_size=64, learning_rate=2e-4):
        super().__init__()
        self.hidden_size = hidden_size
        self.learning_rate = learning_rate

        self.num_classes = 10
        channels, width, height = (1, 28, 28)

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

        self.accuracy = Accuracy('multiclass', num_classes=10)

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

        self.log('val_loss', loss, prog_bar=True)
        self.log('val_acc', self.accuracy, prog_bar=True)
        return loss

    def test_step(self, batch, batch_idx):
        return self.validation_step(batch, batch_idx)

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.learning_rate)
        return optimizer


def main():
    dm = MNISTDataModule()
    model = LitMNIST()

    tqdm_bar = TQDMProgressBar(refresh_rate=20)
    early_stop = EarlyStopping(monitor="val_loss", patience=10, mode="min")

    trainer = pl.Trainer(
        accelerator="auto",
        devices="auto",
        callbacks=[tqdm_bar, early_stop],
        max_epochs=100,
    )
    trainer.fit(model, datamodule=dm)
    trainer.test(datamodule=dm, ckpt_path='best')


if __name__ == '__main__':
    main()
