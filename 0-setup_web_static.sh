#!/usr/bin/env bash
# This script sets up the web servers for deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &>/dev/null; then
    sudo apt-get -y update
    sudo apt-get -y upgrade
    sudo apt-get -y install nginx
fi

# Create necessary directories
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file
echo "<html>\n\t\<head>\n\t\</head>\n\t\<body>\n\t\Holberton School\n\t\</body>\n\t\</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i '38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default
sudo service nginx start
