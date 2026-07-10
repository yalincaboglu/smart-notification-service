#!/bin/bash
set -e

# Update OS packages
yum update -y

# Install Docker, Git, and Python
amazon-linux-extras install docker -y
yum install -y git python3

# Start Docker service
systemctl enable docker
systemctl start docker

# Add ec2-user to the docker group so docker can be used without sudo
usermod -a -G docker ec2-user

# Install Docker Compose plugin
mkdir -p /usr/local/libexec/docker/cli-plugins
curl -SL "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-linux-x86_64" -o /usr/local/libexec/docker/cli-plugins/docker-compose
chmod +x /usr/local/libexec/docker/cli-plugins/docker-compose
ln -sf /usr/local/libexec/docker/cli-plugins/docker-compose /usr/bin/docker-compose

# Clone repository to /home/ec2-user/app
cd /home/ec2-user
if [ ! -d "app" ]; then
  git clone --branch "${repo_branch}" "${repo_url}" app
else
  cd app
  git pull origin "${repo_branch}"
fi

cd /home/ec2-user/app

# Ensure app directory owned by ec2-user
chown -R ec2-user:ec2-user /home/ec2-user/app

# Start Docker Compose stack using the repository's compose file
docker compose --env-file .env.docker up -d --build
