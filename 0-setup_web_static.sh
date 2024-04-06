#!/usr/bin/env bash
# Script for configuring NGINX for serving web_static content

# Install NGINX
sudo apt-get -y update
sudo apt-get -y install nginx

# Set up file structure
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Add test content
echo "This is a test page to verify your Nginx configuration." >> /data/web_static/releases/test/index.html

# Create symbolic link
ln -fs /data/web_static/releases/test/ /data/web_static/current

# Assign ownership to user and group
chown -R ubuntu:ubuntu /data

# Update NGINX configuration to serve content
sed -i "/listen 80 default_server;/a location /hbnb_static {alias /data/web_static/current/;}" /etc/nginx/sites-available/default

# Allow Nginx through firewall
sudo ufw allow "Nginx HTTP"

# Restart NGINX
sudo service nginx restart

exit 0
