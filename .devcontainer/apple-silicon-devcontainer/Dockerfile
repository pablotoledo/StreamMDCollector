# Use the base image from Ubuntu 22.04
FROM --platform=linux/arm64 ubuntu:22.04

# Avoid questions when installing packages
ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies for adding repositories and necessary tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    gnupg \
    ca-certificates \
    build-essential \
    curl \
    git \
    sudo \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    apt-transport-https \
    tree \
    lsb-release

# Add Docker's official GPG key
RUN install -m 0755 -d /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
RUN echo \
    "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null

# Add the deadsnakes PPA
RUN add-apt-repository ppa:deadsnakes/ppa

# Update and install Docker packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin

# Install Python 3.10 and related packages
RUN apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3-pip

# Upgrade pip for Python 3.10
RUN python3.10 -m pip install --upgrade pip

# Install Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs

# Copy and install Python requirements
COPY requirements.txt /tmp/
RUN python3.10 -m pip install -r /tmp/requirements.txt

# Clean up
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add vscode user and configure Docker access
RUN useradd -m vscode \
    && echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    && usermod -aG sudo vscode \
    && usermod -aG docker vscode

# Create symbolic link for docker compose
RUN ln -s /usr/libexec/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose

# Set up working directory
WORKDIR /home/vscode

# Switch to vscode user
USER vscode

# Set up environment
ENV HOME="/home/vscode"
RUN echo 'alias python="python3.10"' >> /home/vscode/.bashrc

# Start a shell
CMD ["/bin/bash"]