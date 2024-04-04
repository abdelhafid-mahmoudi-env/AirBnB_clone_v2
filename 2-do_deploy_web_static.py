#!/usr/bin/python3
"""This module defines a Fabric script."""

from fabric.api import run, env, put
import os.path

# Update with your server IPs
env.hosts = ['52.23.177.252', '18.204.7.7']
env.key_filename = '~/.ssh/school'
env.user = 'ubuntu'


def do_deploy(archive_path):
    """Deploys the archive to the web servers."""

    if not os.path.isfile(archive_path):
        return False
    compressed_file = archive_path.split("/")[-1]
    no_extension = compressed_file.split(".")[0]

    try:
        remote_path = "/data/web_static/releases/{}/".format(no_extension)
        sym_link = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(remote_path))
        run("sudo tar -xvzf /tmp/{} -C {}".format(compressed_file, remote_path))
        run("sudo rm /tmp/{}".format(compressed_file))
        run("sudo mv {}/web_static/* {}".format(remote_path, remote_path))
        run("sudo rm -rf {}/web_static".format(remote_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -sf {} {}".format(remote_path, sym_link))
        return True
    except Exception as e:
        return False
