#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)"""
import os.path
from fabric.api import put, env, run, local
from datetime import datetime
import os

env.hosts = ["52.23.177.252", "18.204.7.7"]

env.user = "ubuntu"


def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)
        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """ deploy package """
    if archive_path is None or not os.path.isfile(archive_path):
        return False

    aname = os.path.basename(archive_path)
    rname = aname.split(".")[0]

    put(local_path=archive_path, remote_path="/tmp/")
    run("mkdir -p /data/web_static/releases/{}".format(rname))
    run("tar -xzf /tmp/{} \
        -C /data/web_static/releases/{}".format(aname, rname))
    run("rm /tmp/{}".format(aname))
    run("rm -rf /data/web_static/current")
    run("ln -fs /data/web_static/releases/{}/ \
        /data/web_static/current".format(rname))
    run("mv /data/web_static/current/web_static/* /data/web_static/current/")
    run("rm -rf /data/web_static/curren/web_static")

    return True


archive = do_pack()


def deploy():
    deploythis = do_deploy(archive)
    return deploythis
