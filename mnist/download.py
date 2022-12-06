from pathlib import Path

import hydra
from torchvision.datasets import MNIST

DIR = Path(__file__).parent


@hydra.main(version_base=None, config_path=str(DIR), config_name='config')
def main(cfg):
    data_dir = DIR / 'data'
    MNIST(str(data_dir), train=True, download=True)
    MNIST(str(data_dir), train=False, download=True)


if __name__ == '__main__':
    main()
