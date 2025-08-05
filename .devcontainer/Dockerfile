FROM mcr.microsoft.com/devcontainers/python:3.11

# Graphvizのシステムパッケージをインストール
RUN apt-get update && apt-get install -y \
    graphviz \
    graphviz-dev \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリの設定
WORKDIR /workspaces/data-analysis-env