import os

import wandb

wandb.init(project="my-awesome-project", name=os.getenv("RUN_NAME"))
