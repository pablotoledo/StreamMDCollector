# Use the base image from Ubuntu 22.04

FROM ubuntu:22.04

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
    tree \
    sudo

# Add the deadsnakes PPA
RUN add-apt-repository ppa:deadsnakes/ppa

# Update the package list after adding PPA
RUN apt-get update

# Install Python 3.10 and related packages
RUN apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-dev \
    python3.10-distutils \
    python3-pip

# Upgrade pip for Python 3.10
RUN python3.10 -m pip install --upgrade pip

# Install pyenv using the recommended method
RUN curl https://pyenv.run | bash
 
# Set up pyenv environment variables
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

# Initialize pyenv in the shell
RUN echo 'export PYENV_ROOT="$PYENV_ROOT"' >> /root/.bashrc \
    && echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /root/.bashrc \
    && echo 'eval "$(pyenv init --path)"' >> /root/.bashrc

# Install Node.js from NodeSource (adjust the version as needed)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs
 
# Install aws-cdk
RUN npm install -g aws-cdk

# Install AWS CLI using npm
RUN apt-get install unzip
RUN curl https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN rm awscliv2.zip


# Copy the requirements.txt file and install Python dependencies using Python 3.10
COPY requirements.txt /tmp/
RUN python3.10 -m pip install -r /tmp/requirements.txt

# Install Docker
RUN apt-get update && apt-get install -y --no-install-recommends \
    docker.io

# Clean up the apt cache and temporary files
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# New docker group
RUN newgrp docker

# Add 'vscode' user and add to sudoers and docker group
RUN useradd -m vscode \
    && echo 'vscode ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
    && usermod -aG sudo,docker vscode

# Change ownership of pyenv to vscode user
RUN chown -R vscode:vscode /root/.pyenv

# Set the default user to vscode
USER vscode

# Set the working directory
WORKDIR /home/vscode

 
# Set the HOME environment variable
ENV HOME="/home/vscode"

# Set up pyenv environment variables for vscode user
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

# Install pyenv using the recommended method, as vscode user
RUN curl https://pyenv.run | bash

# Initialize pyenv in the shell for vscode user
RUN echo 'export PYENV_ROOT="$PYENV_ROOT"' >> $HOME/.bashrc \
    && echo 'export PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"' >> $HOME/.bashrc \
    && echo 'eval "$(pyenv init --path)"' >> $HOME/.bashrc \
    && echo 'eval "$(pyenv init -)"' >> $HOME/.bashrc

RUN echo 'alias python="python3.10"' >> /home/vscode/.bashrc

RUN export DOCKER_BUILDKIT=0

# Start a shell
CMD ["/bin/bash"]