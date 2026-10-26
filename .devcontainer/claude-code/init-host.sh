#!/bin/sh
# Create the host directories that devcontainer.json bind-mounts.
# This script runs on the HOST before the container is created.
# docker refuses to create the container when a bind source is missing, so a
# host that has never run `gh auth login` (no ~/.config/gh) or never run Claude
# Code (no ~/.claude) could not start the container without this.
# mkdir -p is idempotent - it only creates if missing, won't clobber existing.
# Keep this list in step with the ${localEnv:HOME} bind mounts in
# devcontainer.json; test/test_devcontainer.py fails when they drift.

mkdir -p "$HOME/.claude" "$HOME/.config/gh"
