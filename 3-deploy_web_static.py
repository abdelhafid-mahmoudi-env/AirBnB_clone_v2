#!/usr/bin/python3
"""Fabric script that creates and distributes an archive."""

import datetime
import os
from fabric.api import put, env, run, local


# Replace with your server IPs
env.hosts = ["52.23.177.252", "18.204.7.7"]
# Replace with your username
env.user = "ubuntu"

# Global variable to store the path of the created archive
archive_path = None


def do_pack():
    """
    Package function.
    """
    global archive_path
    if archive_path is None:
        if not os.path.isdir("versions"):
            os.makedirs("versions")
        ntime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(ntime)
        local("tar -cvzf {} web_static".format(archive_path))
    return archive_path if os.path.exists(archive_path) else None


def do_deploy(archive_path):
    """
    Deploy package.
    """
    if not os.path.exists(archive_path):
        return False
    aname = os.path.basename(archive_path)
    rname = aname.split(".")[0]

    put(local_path=archive_path, "/tmp/")
    run("mkdir -p /data/web_static/releases/{}/".format(rname))
    run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
        aname, rname))
    run("rm /tmp/{}".format(aname))
    run("mv /data/web_static/releases/{}/web_static/* "
        "/data/web_static/releases/{}/".format(rname, rname))
    run("rm -rf /data/web_static/releases/{}/web_static".format(rname))
    run("rm -rf /data/web_static/current")
    run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(
        rname))
    return True


def deploy():
    """
    Package and deploy to servers.
    """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
