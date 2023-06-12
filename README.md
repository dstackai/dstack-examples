# Examples

Welcome to `dstack-examples`. This repository contains a collection of examples
demonstrating how to use `dstack`.

## Prerequisites

<div class="termy">

```shell
pip install dstack
dstack start
```

The `dstack start` command starts the Hub server, creating the default project that runs dev environments, pipelines,
and apps locally.

> **Note**
> To run dev environments and tasks in the cloud (AWS, GCP, Azure),
> create the corresponding [project](https://dstack.ai/docs/guides/projects/)
> and configure a [profile](https://dstack.ai/docs/#defining-profiles) with required resources.

</div>

### Clone the repo

```shell
git clone https://github.com/dstackai/dstack-examples
cd dstack-examples
dstack init
```

The `dstack-init` command initializes the repository for use with `dstack`.

## How to run examples

| Example                                    | How to run                                  |     | Notes                                                                                                                                    |
|--------------------------------------------|---------------------------------------------|:----|------------------------------------------------------------------------------------------------------------------------------------------|
| **Run a dev environment**                  | `dstack run .`                              |     | Make sure to configure a project and a profile if you plan to use plan to run in the cloud.                                              |
| **Run a FastAPI app**                      | `dstack run fastapi-app/ --reload`          |     |                                                                                                                                          |
| **Train a MNIST model**                    | `dstack run mnist-train/`                   |     |                                                                                                                                          |
| **Train a MNIST model (with Tensorboard)** | `dstack run mnist-train-tensorboard/`       |     |                                                                                                                                          |
| **Run a Stable Diffusion Gradio app**      | `dstack run stable-diffusion-app/ --reload` |     | Requires at least one GPU and minimum `16GB` of RAM. Make sure to configure a project and a profile.                                     |
| **Run a Dolly Gradio app**                 | `dstack run dolly-app/ --reload`            |     | Requires at least one GPU with at least `24GB` of GPU memory and at least `64GB` of RAM. Make sure to configure a project and a profile. |
