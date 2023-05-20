# Examples

Welcome to `dstack-examples`. This repository contains a collection of examples 
demonstrating how to use `dstack`.

## Getting started

If you'd like to run the examples on your own machine, follow these instructions:

### Installation and setup

<div class="termy">

```shell
pip install dstack
dstack start
```

The `dstack start` command starts the Hub server, creating the default project that runs dev environments, pipelines,
and apps locally.

> **Note:**
> To run dev environments, pipelines, and apps in the cloud (AWS, GCP, Azure), log in to Hub, and [configure](http://127.0.0.1:8000/docs/guides/dev-environments/guides/projects) the corresponding project.

</div>

### Clone the repo

```shell
git clone https://github.com/dstackai/dstack-examples
cd dstack-examples
dstack init
```

The `dstack-init` command initializes the repository for use with `dstack`.

## Examples

### Guides

- [Dev environments](dev-environments/README.md)
- [Pipelines](pipelines/README.md)
- [Apps](apps/README.md)

### More examples

#### LLMs

 - [Running your own ChatGPT with Gradio and Dolly](dolly/README.md)
 - [Generating images with Stable Diffusion](stable_diffusion/README.md)

#### Experiment tracking

- [Tracking experiments with TensorBoard](tensorboard/REAMDE.md)
- [Tracking experiments with W&B](wandb/REAMDE.md)