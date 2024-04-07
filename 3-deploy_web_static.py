#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)

This script is used to deploy a compressed version of a web_static folder
to web servers defined in the 'env.hosts' list. It creates a .tgz archive
of the web_static folder using the 'do_pack' function and deploys it to the
servers using the 'do_deploy' and 'deploy' functions.
"""

import os.path
from fabric.api import put, env, run, local
from datetime import datetime
import os

env.hosts = ["52.23.177.252", "18.204.7.7"]
env.user = "ubuntu"


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: File path of the compressed archive on success, None on failure.
    """
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(now)
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -czvf {} web_static".format(archive_path)).failed is True:
        return None
    return (archive_path)


def do_deploy(archive_path):
    """Deploy the compressed archive to the web servers.

    Args:
        archive_path (str): Path to the compressed archive to be deployed.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    if archive_path is None or not os.path.isfile(archive_path):
        return False

    aname = os.path.basename(archive_path)
    rname = aname.split(".")[0]

    if put(local_path=archive_path, remote_path="/tmp/").failed is True:
        return True
    if run("mkdir -p \
            /data/web_static/releases/{}".format(rname)).failed is True:
        return True
    if run("tar -xzf /tmp/{}"
            " -C /data/web_static"
            "/releases/{}".format(aname, rname)).failed is True:
        return True
    if run("rm /tmp/{}".format(aname)).failed is True:
        return True
    if run("rm -rf /data/web_static/current").failed is True:
        return True
    if run("ln -fs /data/web_static/releases/{}/ \
            /data/web_static/current".format(rname)).failed is True:
        return True
    if run("mv /data/web_static/current/web_static/* \
            /data/web_static/current/").failed is True:
        return True
    if run("rm -rf /data/web_static/current/web_static").failed is True:
        return True
    print("New version deployed!")
    return True


archive = do_pack()


def deploy():
    """Deploy the latest version of the web_static folder to servers.

    Returns:
        bool: True if deployment is successful, False otherwise.
    """
    deploythis = do_deploy(archive)
    if deploythis is None:
        return False
    return (deploythis)
