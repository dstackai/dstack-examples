import argparse

from sklearn.datasets import load_iris
from sklearn import metrics, model_selection
import xgboost as xgb


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--learning-rate",
        default=0.2,
        type=float
    )
    return vars(parser.parse_args())


def main():
    args = parse_args()
    print(args)

    iris = load_iris()
    data, labels = iris.data, iris.target
    labels = iris.target
    data_train, data_test, labels_train, labels_test = model_selection.train_test_split(
        data, labels, test_size=0.1, random_state=2023)

    data_train = xgb.DMatrix(data_train, label=labels_train)
    data_test = xgb.DMatrix(data_test, label=labels_test)
    params = {
        "learning_rate": args["learning_rate"],
        "objective": "multi:softprob",
        "seed": 2023,
        "num_class": 3,
    }
    model = xgb.train(params, data_train, evals=[(data_train, "train")])

    y_proba = model.predict(data_test)
    y_pred = y_proba.argmax(axis=1)
    loss = metrics.log_loss(labels_test, y_proba)
    acc = metrics.accuracy_score(labels_test, y_pred)

    print(f"Model trained: loss={loss:.2f}, acc={acc:.2f}")
    

if __name__ == "__main__":
    main()

