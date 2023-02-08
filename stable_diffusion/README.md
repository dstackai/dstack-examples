# Tutorial: Stable Diffusion with 🧨 Diffusers and dstack

This tutorial will demonstrate how to generate images using Stable Diffusion with the help of
the [`diffusers`](https://github.com/huggingface/diffusers) and [`dstack`](https://github.com/dstackai/dstack)
libraries.

The `diffusers` library is a convenient tool that enables you to load pretrained diffusion models and perform inference
and fine-tuning with just one command.

On the other hand, `dstack` is a lightweight tool that enables you to define ML workflows in a reproducible manner.
Additionally, it allows you to run these workflows either locally or in the cloud with a single command.

By the end of this tutorial, you will have learned how to use both `diffusers` and `dstack` to generate images with
Stable Diffusion.

## Requirements

Here is the list of Python libraries that we will utilize:

```txt
diffusers
transformers
scipy
ftfy
accelerate
safetensors
```

> **Note**
> 
> We're using the [`safetensors`](https://github.com/huggingface/safetensors) library because it implements a new simple format for storing tensors safely (as opposed
> to pickle) and that is still fast (zero-copy).

"To ensure our scripts can run smoothly across all environments, let's include them in
the `stable_diffusion/requirements.txt` file.

You can also install these libraries locally:

```shell
pip install -r stable_diffusion/requirements.txt
```

Also, because we'll use `dstack` CLI, let's install it locally:

```shell
pip install dstack -U
```

## Download the pre-trained model

In our tutorial, we'll use the [`runwayml/stable-diffusion-v1-5`](https://huggingface.co/runwayml/stable-diffusion-v1-5) model (pretrained by Runway).

Let's create the following `stable_diffusion/stable_diffusion.py` file:

```python
import shutil

from diffusers import StableDiffusionPipeline


def main():
    _, cache_folder = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5",
                                                              return_cached_folder=True)
    shutil.copytree(cache_folder, "./models/runwayml/stable-diffusion-v1-5", dirs_exist_ok=True)
```

> **Note**
> 
> By default, `diffusers` downloads the model to its own [cache folder](https://huggingface.co/docs/datasets/cache) built using symlinks.
> Since `dstack` doesn't support symlinks in artifacts, we're copying the model files to the local `models` folder. 

In order to run a script via `dstack`, the script must be defined as a workflow via a YAML file
under `.dstack/workflows`.

Let's define the following `.dstack/workflows/stable_diffusion.yaml` file:

```yaml
workflows:
  - name: stable-diffusion
    provider: bash
    commands:
      - pip install -r stable_diffusion/requirements.txt
      - python stable_diffusion/stable_diffusion.py
    artifacts:
      - path: ./models
    resources:
      memory: 16GB
```

Now, the workflow can be run anywhere via the `dstack` CLI.

> **Note**
> 
> Before you run a workflow via `dstack`, make sure your project has a remote Git branch configured,
> and invoke the `dstack init` command which will ensure that `dstack` may access the repository:
> ```shell
> dstack init
> ```

Here's how to run a `dstack` workflow locally:

```shell
dstack run stable-diffusion
```

Once you run it, `dstack` will run the script, and save the `models` folder as an artifact.
After that, you can reuse it in other workflows.

## Attach an interactive IDE

Sometimes, before you can run a workflow, you may want to run code interactively,
e.g. via an IDE or a notebook.

Look at the following example:

```yaml
workflows:
  - name: code-stable
    provider: code
    deps:
      - workflow: stable-diffusion
    setup:
      - pip install -r stable_diffusion/requirements.txt
    resources:
      memory: 16GB
```

As you see, the `code-stable` workflow refers the `stable-diffusion` workflow as a dependency.

If you run it, `dstack` will run a VS Code application with the code, pretrained model,
and Python environment:

```shell 
dstack run code-stable
```

## Generate images

Let's write a script that generates images using a pre-trained model and given prompts.

Here's an example of the `stable_diffusion/prompt_stable.py` file:

```python
import argparse
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--prompt", action='append', required=True)
    args = parser.parse_args()

    pipe = StableDiffusionPipeline.from_pretrained("./models/runwayml/stable-diffusion-v1-5", local_files_only=True)
    if torch.cuda.is_available():
        pipe.to("cuda")
    images = pipe(args.prompt).images

    output = Path("./output")
    output.mkdir(parents=True, exist_ok=True)
    for i in range(len(images)):
        images[i].save(output / f"{i}.png")
```

The script loads the model from the local `models` folder, generates images and saves them to the 
local `output` folder.

To be able to run it via `dstack`, let's define it in `.dstack/workflows/stable_diffusion.yaml`:

```yaml
workflows:
  - name: prompt-stable
    provider: bash
    deps:
      - workflow: stable-diffusion
    commands:
      - pip install -r stable_diffusion/requirements.txt
      - python stable_diffusion/prompt_stable.py ${{ run.args }}
    artifacts:
      - path: ./output
    resources:
      memory: 16GB
```

> **Note**
> 
> The `dstack run` command allows to pass arguments to the workflow via `${{ run.args }}`.

Let's run the workflow locally:

```shell
dstack run prompt-stable -P "a photo of an astronaut riding a horse on mars" 
```

## Configure a remote

By default, workflows in `dstack` run locally. However, you have the option to configure a `remote` to run your
workflows.
For instance, you can set up your AWS account as a `remote` to execute workflows.

To configure a `remote`, run the following command:

```shell
dstack config
```

This command prompts you to select an AWS profile for credentials, an AWS region for workflow execution, and an S3
bucket to store remote artifacts.

```shell
AWS profile: default
AWS region: eu-west-1
S3 bucket: dstack-142421590066-eu-west-1
EC2 subnet: none
```

Once a remote is configured, you can use the `--remote` flag with the `dstack run` command
to run workflows remotely.

Let's first run the `stable-diffusion` workflow:

```shell
dstack run stable-diffusion --remote
```

Now, you can run the `prompt-stable` remotely as well:

```shell
dstack run prompt-stable --remote --gpu-name V100 -P "a photo of an astronaut riding a horse on mars"
```

> **Note**
> 
> You can configure the required resources to run the workflows either via the `resources` property in YAML
> or the `dstack run` command's arguments, such as `--gpu`, `--gpu-name`, etc.

When you run a remote workflow, `dstack` automatically creates resources in the configured cloud,
and releases them once the workflow is finished.

That's all there is to it. If you found the tutorial interesting, you can delve deeper by exploring the official documentation
for [`diffusers`](https://huggingface.co/docs/diffusers/index) and [`dstack`](https://docs.dstack.ai). 

The source code for this tutorial can be located on [GitHub](https://github.com/dstackai/dstack-examples/tree/main/stable_diffusion).