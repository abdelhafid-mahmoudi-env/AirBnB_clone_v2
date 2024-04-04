#!/usr/bin/python3
"""
This module defines a Fabric script that distributes an archive to web servers.
"""

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['52.23.177.252', '	18.204.7.7']  # Update with your server IPs

def do_deploy(archive_path):
    """
    Deploys the archive to the web servers.
    """
    if not exists(archive_path):
        return False
    try:
        # Extract the archive filename and the filename without the extension
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/{}'.format(file_name))

        # Uncompress the archive to the folder on the web server
        run('mkdir -p /data/web_static/releases/{}/'.format(name))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(file_name, name))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(file_name))

        # Move the content of the web static to the parent directory and delete the directory
        run('mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/'.format(name, name))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(name))

        # Delete the symbolic link and create a new one
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'.format(name))

        print("New version deployed!")
        return True
    except Exception as e:
        return False
