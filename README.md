# Examples

Welcome to `dstack-examples`. This repository contains a collection of examples
demonstrating how to use `dstack`.

## 1. Setup

```shell
pip install "dstack[all]" -U
dstack start
```

The `dstack start` command starts the Hub server, creating the default project that runs dev environments, pipelines,
and apps locally.

## 2. Projects

To run examples in the cloud (AWS, GCP, Azure, Lambda Cloud),
make sure to create the corresponding [project](https://dstack.ai/docs/guides/projects/)
via the UI.

## 3. Clone the repo

```shell
git clone https://github.com/dstackai/dstack-examples
cd dstack-examples
dstack init
```

## 4. Run examples

| Example                             | How to run                                                                  |
| ----------------------------------- | --------------------------------------------------------------------------- |
| **Default dev environment**         | `dstack run . --gpu 16GB`                                                   |
| **Deploying LLMs using vLLM**       | `dstack run . -f vllm/serve.dstack.yml --gpu 24GB`                          |
| **Deploying LLMs using TGI**        | `dstack run . -f text-generation-inference/serve.dstack.yml --gpu 24GB`     |
| **Custom dev environment for TGI**  | `dstack run . -f text-generation-inference/.dstack.yml --build  --gpu 24GB` |
| **Deploying SDXL using FastAPI**    | `dstack run . -f stable-diffusion-xl/api.dstack.yml --gpu 16GB`             |
| **Fine-tuning Llama 2 using QLoRA** | `dstack run . -f llama-2/train.dstack.yml  --gpu 16GB`                      |
| **Deploying LLMs using Python API** | `streamlit run deploy-python/app.py`                                        |