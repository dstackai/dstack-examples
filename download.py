import torchvision as torchvision
import torchvision.transforms as T

if __name__ == '__main__':
    torchvision.datasets.MNIST(root="data", train=True, transform=T.ToTensor(), download=True)
