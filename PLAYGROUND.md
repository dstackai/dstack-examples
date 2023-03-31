# dstack Playground

Welcome to `dstack`'s Playground.

Once `dstack` is installed and ready, execute the commands below to navigate through the examples.

### 1. Init

Make sure to initialize the working directory before running any workflows.

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

Run this workflow using the `dstack run` command:

```shell
dstack run hello
```

This command runs the workflow on your local machine by default. However, you will eventually have the option to
configure a remote and run the workflow remotely (e.g. in a configured cloud account).