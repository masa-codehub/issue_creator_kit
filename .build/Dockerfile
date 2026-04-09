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
    unzip \
    zlib1g-dev \
    openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# 3. OPA (Open Policy Agent) のインストール
RUN curl -L -o /usr/local/bin/opa https://openpolicyagent.org/downloads/latest/opa_linux_$(dpkg --print-architecture)_static \
    && chmod 755 /usr/local/bin/opa

# 4. Structurizr CLI のインストール
RUN curl -L -o structurizr-cli.zip https://github.com/structurizr/cli/releases/download/v2024.03.03/structurizr-cli.zip \
    && unzip structurizr-cli.zip -d /usr/local/bin/structurizr-cli \
    && rm structurizr-cli.zip \
    && ln -s /usr/local/bin/structurizr-cli/structurizr.sh /usr/local/bin/structurizr

# 5. GitHub CLI のインストール (wgetを使わずcurlで実行)
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

# 5. Gemini CLI のインストール (latest指定)
RUN npm install -g @google/gemini-cli@latest

# 7. キャッシュディレクトリの確保
ENV UV_CACHE_DIR=/root/.cache/uv

CMD ["/bin/bash"]