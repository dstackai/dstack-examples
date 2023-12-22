# Examples

Welcome to `dstack-examples`. This repository contains a collection of examples
demonstrating how to use `dstack`.

## 1. Setup

### 1.1. Install dstack

```shell
pip install "dstack[all]" -U
```

### 1.2 Configure clouds

Configure cloud credentials in `~/.dstack/server/config.yml`. [Learn more](https://dstack.ai/docs/config/server/).

### 1.3. Start the server

```shell
dstack server
```

## 2. Run examples

### 2.1. Init the repo

```shell
git clone https://github.com/dstackai/dstack-examples
cd dstack-examples
dstack init
```

### 2.2. Run a dev environment

Here's how to run a dev environment with the current repo:

```shell
dstack run . --gpu 24GB
```

### 2.3. Run any example

Here's how any example can be run:

```shell
dstack run . -f deployment/vllm/serve.dstack.yml --gpu 24GB
```

### More information

- [Docs](https://dstack.ai/docs)
- [See all learning materials](https://dstack.ai/learn)