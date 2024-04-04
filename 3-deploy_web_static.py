#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""

from fabric.api import env, local, put, run
import os
from datetime import datetime

env.hosts = ['52.23.177.252', '18.204.7.7']
env.key_filename = '~/.ssh/school'
env.user = 'ubuntu'

def do_pack():
    """Generates a .tgz archive from the contents of the 'web_static' folder."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None

def do_deploy(archive_path):
    """Deploys an archive to the web servers."""
    if not os.path.exists(archive_path):
        return False
    try:
        basename = os.path.basename(archive_path)
        name = basename.split('.')[0]
        tmp_path = "/tmp/{}".format(basename)
        dest_path = "/data/web_static/releases/{}".format(name)
        put(archive_path, tmp_path)
        run("mkdir -p {}".format(dest_path))
        run("tar -xzf {} -C {}".format(tmp_path, dest_path))
        run("rm {}".format(tmp_path))
        run("mv {}/web_static/* {}".format(dest_path, dest_path))
        run("rm -rf {}/web_static".format(dest_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(dest_path))
        return True
    except Exception:
        return False

def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

if __name__ == "__main__":
    deploy()
