from train import DIR, MNISTDataModule
import hydra


@hydra.main(version_base=None, config_path=DIR, config_name='config')
def main(cfg):
    dm = MNISTDataModule(**cfg.datamodule)
    dm.prepare_data()


if __name__ == '__main__':
    main()