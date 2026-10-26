# rerun_examples
A template repo for python projects that is set up using [pixi](https://pixi.sh). 

This has basic setup for

* ruff (formatting and linting)
* pytest
* git-lfs
* basic github actions ci
* pulling updates from this template
* codecov
* pypi upload
* dependabot

## One ruff version

Ruff is pinned once, as `ruff==X.Y.Z` in `pyproject.toml`. Everything else runs that ruff from the pixi environment:

* `pixi run lint` and `pixi run ci` run `ruff check .` and `ruff format --check .`
* the prek hooks in `.pre-commit-config.yaml` are `repo: local` hooks that run `pixi run --locked ruff ...`, so they carry no version of their own
* CI (`ci.yml` and `prek.yaml`) installs the pixi environment with `setup-pixi` and `locked: true`, so CI fails when `pixi.lock` does not match `pyproject.toml`. It does not run a stale ruff.

To change the ruff version, edit the pin in `pyproject.toml` and run `pixi lock`. Dependabot changes only `pyproject.toml`, so run `pixi lock` on its PR before you merge it. Do not add a `rev:` for ruff to `.pre-commit-config.yaml` or a `version:` to a ruff GitHub action. Child repos pick this setup up through `pixi run update-from-template-repo`.

## Continuous Integration Status

[![Ci](https://github.com/blooop/rerun_examples/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/blooop/rerun_examples/actions/workflows/ci.yml?query=branch%3Amain)
[![Codecov](https://codecov.io/gh/blooop/rerun_examples/branch/main/graph/badge.svg?token=Y212GW1PG6)](https://codecov.io/gh/blooop/rerun_examples)
[![GitHub issues](https://img.shields.io/github/issues/blooop/rerun_examples.svg)](https://GitHub.com/blooop/rerun_examples/issues/)
[![GitHub pull-requests merged](https://badgen.net/github/merged-prs/blooop/rerun_examples)](https://github.com/blooop/rerun_examples/pulls?q=is%3Amerged)
[![GitHub release](https://img.shields.io/github/release/blooop/rerun_examples.svg)](https://GitHub.com/blooop/rerun_examples/releases/)
[![License](https://img.shields.io/github/license/blooop/rerun_examples)](https://opensource.org/license/mit/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)](https://www.python.org/downloads/)
[![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)


# Install

There are two methods of using this project.  

1. Use github to use this project as a template
2. Clone the project and run, `scripts/update_from_template.sh` and then run the `scripts/rename_project.sh` to rename the project.

If you want to use docker you may want to run the `scripts/setup_host.sh` script.  It will set up docker and the NVIDIA Container Toolkit (tested on ubuntu 22.04/24.04/26.04).

If you are using pixi, look at the available tasks in pyproject.toml  If you are new to pixi follow the instructions on the pixi [website](https://prefix.dev/)

# Claude Code Online Support

This template includes built-in support for [Claude Code](https://docs.claude.com/claude-code) online environment! The `.claude/hooks/SessionStart` script automatically:

- Installs pixi package manager
- Sets up all project dependencies
- Configures prek hooks
- Prepares the development environment

**Quick Start with Claude Code:**
1. Open this repository in Claude Code online
2. The environment sets up automatically via the SessionStart hook
3. Claude can immediately run commands like `pixi run test`, `pixi run lint`, etc.

**Manual activation (if needed):**
```bash
source .claude/activate.sh
```

See [.claude/README.md](.claude/README.md) for detailed information about the Claude Code configuration.

# Devcontainer

The devcontainer uses the prebuilt image from the template repository (`ghcr.io/blooop/python_template/devcontainer:latest`) for fast startup. This repo does not carry the template's `.devcontainer/Dockerfile` or the `dev-use-local` / `dev-use-prebuilt` tasks; to build the image locally, bring them over from [blooop/python_template](https://github.com/blooop/python_template) first.

# Github setup

There are github workflows for CI, codecov and automated pypi publishing in `ci.yml` and `publish.yml`.

ci.yml uses pixi tasks to set up the environment matrix and run the various CI tasks. To set up codecov on github, you need to get a `CODECOV_TOKEN` and add it to your actions secrets.

publish.yml uses [pypy-auto-publish](https://github.com/marketplace/actions/python-auto-release-pypi-github) to automatically publish to pypi if the package version number changes. You need to add a `PYPI_API_TOKEN` to your github secrets to enable this.     


# Usage

There are currently two ways of running code.  The preferred way is to use pixi to manage your environment and dependencies. 

```bash
cd project

$pixi run ci
pixi run arbitrary_task
```

If you have dependencies or configuration that cannot be managed by pixi, you can use alternative tools:

- [rockerc](https://github.com/blooop/rockerc): A command-line tool for dynamically creating docker containers with access to host resources such as GPU and 
- [rockervsc](https://github.com/blooop/rockervsc): A Visual Studio Code extension that integrates rockerc functionality into [vscode remote containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

These tools help you create isolated environments with specific dependencies, ensuring consistent setups across different machines.

```bash
cd project_name

rockerc # build and launch container with dependencies set up
# OR
rockervsc # build container, launch and attach vscode to that container.

#once you are inside the container you can use the pixi workflows.
pixi run ci
```

## Legacy

If you don't want to install rocker on your system but want to use vscode, you can run the `scripts/launch_vscode.sh` script to build and connect to a docker container. It will install rocker in a venv.  The docker container is dynamically generated using [rocker](https://github.com/osrf/rocker) and the configuration in `rockerc.yaml`. 

## Troubleshooting

The main pixi tasks are related to CI.  Github actions runs the pixi task "ci".  The CI is mostly likely to fail from a lockfile mismatch.  Use `pixi run fix` to fix any lockfile related problems. 

## vscode tasks

There are two core tasks.  

1. set \<cfg\> from active file

    This sets \<cfg\> to the currently opened file in the editor

2. run \<cfg\>

    This runs python with the file set in \<cfg\>
