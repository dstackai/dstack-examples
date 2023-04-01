from torchvision.datasets import MNIST

if __name__ == '__main__':
    # Download train data
    MNIST("./data", train=True, download=True)
    # Download test data
    MNIST("./data", train=False, download=True)