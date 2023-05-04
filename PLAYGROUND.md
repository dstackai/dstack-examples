# dstack Playground

Welcome to `dstack`'s Playground.

Once `dstack` is installed, use the commands below to walk through the examples.

### Prerequisites

To use `dstack`, we'll need the Hub application up and running. Let's run it as a background process with the following
command:

```shell
dstack start &
```

On startup, the Hub application creates the default project allowing us to run workflows locally.

Finally, we need to initialize the current working directory with the following command:

```shell
dstack init
```

### 1. Hello world

Review the [hello.yaml](.dstack/workflows/hello.yaml) file containing the `hello` workflow, which prints the message 
`"Hello, world!"`.

```yaml
workflows:
  - name: hello
    provider: bash
    commands:
      - echo "Hello, world!"
```

Run it using the `dstack run` command:

```shell
dstack run hello
```

### 2. Python

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

Run it using the `dstack run` command:

```shell
dstack run hello-pandas
```

### 3. Conda

Alternatively to `pip`, you can install packages with `conda`.

Review the [conda.yaml](.dstack/workflows/conda.yaml) file containing the `hello-conda` workflow, which
runs [hello_pandas.py](usage/python/hello_pandas.py).

```yaml
workflows:
  - name: hello-conda
    provider: bash
    commands:
      - conda install pandas -y
      - python usage/python/hello_pandas.py
```

Run it using the `dstack run` command:

```shell
dstack run hello-conda
```

### 4. Artifacts

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

Run it using the `dstack run` command:

```shell
dstack run hello-txt
```

To see artifacts of a run, use the `dstack ls` command followed by the name of the run.

### 5. Deps

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

Run it using the `dstack run` command:

```shell
dstack run cat-txt-2
```

If you don't want to refer to the last run of the workflow but a specific one, you can use [tags](https://docs.dstack.ai/usage/deps/#tags).

### 6. Apps

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

Run it using the `dstack run` command:

```shell
dstack run hello-fastapi
```

### 7. Secrets

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

### 8. Args

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

Run it using the `dstack run` command:

```shell
dstack run hello-args 'Hello, world!'
```

### 9. Providers

`dstack` supports [`bash`](https://docs.dstack.ai/reference/providers/bash), [`docker`](https://docs.dstack.ai/reference/providers/docker), 
[`code`](https://docs.dstack.ai/reference/providers/code), [`lab`](https://docs.dstack.ai/reference/providers/lab), 
and [`notebook`](https://docs.dstack.ai/reference/providers/notebook) [providers](https://docs.dstack.ai/reference/providers/bash). 

Each workflow defined under `.dstack/workflows` must specify a provider.

Alternatively, instead of defining workflows via YAML, you can also run providers directly:

```shell
dstack run bash -c 'echo "Hello, world!"'
```

### 10. Projects

The default project runs workflows locally. However, with the Hub application, you can create
additional projects and configure them to run workflows in the cloud.

To access the Hub application, click on the URL displayed above the `dstack start` command.

Once you have created a project, make sure to configure the CLI to use it by running the `dstack config` command.

> You can configure multiple projects and use them interchangeably (by passing the `--project` argument to the `dstack run`
> command. Any project can be set as the default by passing `--default` to the `dstack config` command.

### 11. Resources

If your project is configured to use cloud,
you can specify which `resources` to use, such as GPU and memory, spot instances, etc.

Review the [resources.yaml](.dstack/workflows/resources.yaml) file containing the `gpu-v100` workflow, which 
requests a `V100` GPU and invokes the `nvidia-smi` command.

```yaml
workflows:
  - name: gpu-v100
    provider: bash
    commands:
      - nvidia-smi
    resources:
      gpu:
        name: V100
        count: 1
```

Run it using the `dstack run` command.

```shell
dstack run gpu-v100
```

When you run it, the Hub application will automatically create the necessary cloud resources to execute the workflow and
tear them down once it is finished.

> **Note:**
> If the corresponding project is not configured as the default, you may 
> need to pass the name of the project with the `--project` argument to `dstack run`.

### What's next?

1. Go ahead try [Quick start](https://dstack.ai/docs/quick-start) on your local machine.
2. Check the [docs](https://dstack.ai/docs) and [tutorials](https://dstack.ai/tutorials/dolly).
3. Join our community on our [Slack channel](https://join.slack.com/t/dstackai/shared_invite/zt-xdnsytie-D4qU9BvJP8vkbkHXdi6clQ).