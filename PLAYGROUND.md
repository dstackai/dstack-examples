# dstack Playground

Welcome to `dstack`'s Playground.

Once `dstack` is installed, use the commands below to walk through the examples.

### 1. Init

Make sure to initialize the working directory before running any further commands.

```shell
dstack init
```

### 2. Hello world

Review the [hello.yaml](.dstack/workflows/hello.yaml) file containing the `hello` workflow, which prints the message 
`"Hello, world!"`.

```yaml
workflows:
  - name: hello
    provider: bash
    commands:
      - echo "Hello, world!"
```

Run this workflow locally using the `dstack run` command:

```shell
dstack run hello
```

Later, we'll see how to configure a remote (using the `dstack config` command) to run the workflow remotely (e.g. in a configured cloud account).

### 3. Python

Review the [python.yaml](.dstack/workflows/python.yaml) file containing the `hello-pandas` workflow, which
runs [hello_pandas.py](usage/python/hello_pandas.py).

```yaml
workflows:
  - name: hello-pandas
    provider: bash
    commands:
      - pip install pandas
      - python python/hello_pandas.py
```

Run this workflow locally using the `dstack run` command:

```shell
dstack run hello-py
```

### 4. Conda

Alternatively to `pip`, you can install packages with `conda`.

Review the [conda.yaml](.dstack/workflows/conda.yaml) file containing the `hello-conda` workflow, which
runs [hello_pandas.py](usage/python/hello_pandas.py).

```yaml
workflows:
  - name: hello-conda
    provider: bash
    commands:
      - conda install pandas
      - python python/hello_pandas.py
```

Run this workflow locally using the `dstack run` command:

```shell
dstack run hello-conda
```

### 5. Artifacts

Review the [artifacts.yaml](.dstack/workflows/artifacts.yaml) file containing the `hello-txt` workflow, 
which creates the local `output/hello.txt` file and saves it as an artifact.

```yaml
workflows:
  - name: hello-txt
    provider: bash
    commands:
      - echo "Hello world" > output/hello.txt
    artifacts:
      - path: ./output
```

Run this workflow locally using the `dstack run` command:

```shell
dstack run hello-txt
```

To see artifacts of a run, use the `dstack ls` command followed by the name of the run.

### 6. Deps

Review the [deps.yaml](.dstack/workflows/deps.yaml) file containing the `cat-txt-2` workflow, 
which reuses the artifacts of the `hello-txt` workflow.

```yaml
workflows:
  - name: cat-txt-2
    provider: bash
    deps:
      - workflow: hello-txt
    commands:
      - cat output/hello.txt
```

Run this workflow locally using the `dstack run` command:

```shell
dstack run cat-txt-2
```

If you don't want to refer to the last run of the workflow but a specific one, you can use [tags](https://docs.dstack.ai/usage/deps/#tags).

### 7. Remotes

By default, workflows run locally. To run workflows remotely, you need to first configure a remote using the [`dstack
config`](https://docs.dstack.ai/reference/cli/config/) command. 

```shell
dstack config
```

> **Note**
> To use AWS or GCP as a remote, the corresponding cloud credentials must be
> configured locally.

Once a remote is configured, use the `--remote` flag with the `dstack run` command to run a workflow in
the remote.

```shell
dstack run hello --remote
```

### 8. Resources

When running a workflow remotely, you can specify which [resources](https://docs.dstack.ai/reference/providers/bash/#resources) to use, such as GPU and memory.

Review the [resources.yaml](.dstack/workflows/resources.yaml) file containing the `gpu-default` workflow, which 
uses `nvidia-smi` to show the available GPU.

```yaml
workflows:
  - name: gpu-default
    provider: bash
    commands:
      - nvidia-smi
    resources:
      gpu: 1
```

Run this workflow locally using the `dstack run` command:

```shell
dstack run gpu-default
```

### 9. Providers

`dstack` supports [`bash`](https://docs.dstack.ai/reference/providers/bash), [`docker`](https://docs.dstack.ai/reference/providers/docker), 
[`code`](https://docs.dstack.ai/reference/providers/code), [`lab`](https://docs.dstack.ai/reference/providers/lab), 
and [`notebook`](https://docs.dstack.ai/reference/providers/notebook) providers. 

You can use the `dstack run` command to run a workflow (defined under [.dstack/workflows](.dstack/workflows)),
or run a provider directly.

Run this workflow locally using the `dstack run` command:

```shell
dstack run bash -c 'echo "Hello, world!"'
```

### 10. Apps

Workflow can host apps. To do this, use `ports` and specify the number ports needed to host apps.
The port numbers will be passes to the workflow via environment variables `PORT_0`, `PORT_1`, etc.

Review the [apps.yaml](.dstack/workflows/apps.yaml) file containing the `hello-fastapi` workflow, which 
runs a FastAPI application.

```yaml
workflows:
  - name: hello-fastapi
    provider: bash
    ports: 1
    commands:
      - pip install fastapi uvicorn
      - uvicorn apps.hello_fastapi:app --port $PORT_0 --host 0.0.0.0
```

Run this workflow locally using the `dstack run` command:

```shell
dstack run hello-fastapi
```

### 11. Secrets

Secrets enable accessing passwords and secure tokens from workflows without embedding them in the code.

You can configure secrets using the [`dstack secrets`](https://docs.dstack.ai/reference/cli/secrets) command.

Run the following command to add a secret:

```shell
dstack secrets add MY_SECRET_TOKEN 42
```

The secret will be passed to workflows as environment variables.

Run the following command to test it:

```shell
dstack run bash -c 'echo $MY_SECRET_TOKEN'
```

### 12. Args

If you pass any arguments to the dstack run command, they can be accessed from the workflow YAML file via the `${{ run.args }}` expression.

Review the [args.yaml](.dstack/workflows/args.yaml) file containing the `hello-args` workflow, which 
pass arguments to [hello-arg.py](usage/args/hello_args.py).

```yaml
workflows:
  - name: hello-args
    provider: bash
    commands:
      - python usage/args/hello_arg.py ${{ run.args }}
```

Run this workflow locally using the `dstack run` command:

```shell
dstack run hello-args 'Hello, world!'
```

### What's next?

1. Go ahead and [install](https://docs.dstack.ai/installation) `dstack` on your local machine.
2. Check the [Quick start](https://docs.dstack.ai/quick-start),
  [Tensorboard](https://docs.dstack.ai/tutorials/tensorboard),
  [Stable Diffusion](https://docs.dstack.ai/tutorials/stable-diffusion), and
  [Weights & Biases](https://docs.dstack.ai/tutorials/wandb) tutorials.
3. Join our community on our [Slack channel](https://join.slack.com/t/dstackai/shared_invite/zt-xdnsytie-D4qU9BvJP8vkbkHXdi6clQ).