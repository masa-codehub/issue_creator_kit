# 1. ベースイメージ: ubuntu:latest
FROM ubuntu:latest

# ★ uv のインストール
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# ビルド時の対話防止とPython設定
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 2. 必須ツールと依存関係のインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    gettext-base \
    git \
    gnupg \
    jq \
    libicu-dev \
    libssl-dev \
    lsb-release \
    procps \
    sudo \
    tar \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. GitHub CLI のインストール (wgetを使わずcurlで実行)
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" > /etc/apt/sources.list.d/github-cli.list \
    && apt-get update && apt-get install -y --no-install-recommends gh \
    && rm -rf /var/lib/apt/lists/*    && apt-get update && apt-get install -y gh \
    && rm -rf /var/lib/apt/lists/*

# 4. Node.js のインストールと npm のアップデート
RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm@latest \
    && rm -rf /var/lib/apt/lists/*

# 5. Gemini CLI のインストール (preview指定)
RUN npm install -g @google/gemini-cli@preview

# 7. キャッシュディレクトリの確保
ENV UV_CACHE_DIR=/root/.cache/uv

CMD ["/bin/bash"]