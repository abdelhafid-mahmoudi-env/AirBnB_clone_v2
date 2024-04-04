#!/usr/bin/env bash
# This script sets up the web servers for deployment of web_static

# Install Nginx if not already installed
# Install Nginx if not already installed
if ! command -v nginx &>/dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
    sudo ufw allow 'Nginx HTTP'
fi

# Remove existing directory if it exists
sudo rm -rf /data/web_static/

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared /data/web_static/current

# create file named index.html
sudo touch /data/web_static/releases/test/index.html

# Create a fake HTML file
echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link, deleting and recreating if already exists
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config="location /hbnb_static { alias /data/web_static/current/; index index.html index.htm; }"
sudo sed -i "/^http {/a $config" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
