#!/usr/bin/python3
"""This module defines a Fabric script."""

from fabric.api import env, put, run
from os.path import exists

# Update with your server IPs
env.hosts = ['52.23.177.252', '18.204.7.7']


def do_deploy(archive_path):
    """Deploys the archive to the web servers."""

    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        put(archive_path, f'/tmp/{file_name}')
        run(f'mkdir -p /data/web_static/releases/{name}/')
        run(
            f'tar -xzf /tmp/{file_name} -C /data/web_static/releases/{name}/'
        )
        run(f'rm /tmp/{file_name}')
        run(
            f'mv /data/web_static/releases/{name}/web_static/* '
            f'/data/web_static/releases/{name}/'
        )
        run(f'rm -rf /data/web_static/releases/{name}/web_static')
        run('rm -rf /data/web_static/current')
        run(
            f'ln -s /data/web_static/releases/{name}/ /data/web_static/current'
        )
        return True
    except Exception:
        return False
