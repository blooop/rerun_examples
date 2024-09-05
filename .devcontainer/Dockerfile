FROM ubuntu:22.04

RUN apt-get update && apt-get install -y jq git-lfs python3-pip libgtk-3-dev libxkbcommon-x11-0 vulkan-tools
RUN python3 -m pip install rerun-sdk==0.18.2

RUN apt-get update && apt-get install -y curl

RUN curl -Ls \
    "https://github.com/prefix-dev/pixi/releases/download/v0.29.0/pixi-$(uname -m)-unknown-linux-musl" \
    -o /pixi && chmod +x /pixi