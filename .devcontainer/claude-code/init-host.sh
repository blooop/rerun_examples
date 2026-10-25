#!/bin/sh
# Create the host directories that devcontainer.json bind-mounts; docker
# refuses to create the container when a bind source is missing.
# This script runs on the HOST before the container is created.
# mkdir -p is idempotent - it only creates if missing, won't clobber existing.

mkdir -p "$HOME/.claude" "$HOME/.config/gh"
