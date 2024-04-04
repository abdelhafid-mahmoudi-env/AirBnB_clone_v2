#!/usr/bin/python3
"""This module defines a Fabric script."""

from fabric.api import env, put, run
from os.path import exists

# Update with your server IPs
env.hosts = ['52.23.177.252', '18.204.7.7']


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
        put(archive_path, f'/tmp/{file_name}')

        # Uncompress the archive to the folder on the web server
        run(f'mkdir -p /data/web_static/releases/{name}/')
        run(
            f'tar -xzf /tmp/{file_name} -C /data/web_static/releases/{name}/'
        )

        # Delete the archive from the web server
        run(f'rm /tmp/{file_name}')

        # Move the content of the web static to the parent directory and
        # delete the directory
        run(
            f'mv /data/web_static/releases/{name}/web_static/* '
            f'/data/web_static/releases/{name}/'
        )
        run(f'rm -rf /data/web_static/releases/{name}/web_static')

        # Delete the symbolic link and create a new one
        run('rm -rf /data/web_static/current')
        run(
            f'ln -s /data/web_static/releases/{name}/ /data/web_static/current'
        )

        print("New version deployed!")
        return True
    except Exception:
        return False
