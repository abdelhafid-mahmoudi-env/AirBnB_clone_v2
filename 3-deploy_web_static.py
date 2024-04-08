#!/usr/bin/python3
"""deploy a compressed version of a web_static folder to web servers"""

import os.path
from fabric.api import put, env, run, local, runs_once
from datetime import datetime
import os


env.hosts = ["52.23.177.252", "18.204.7.7"]
env.user = "ubuntu"


@runs_once
def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = "versions/web_static_{}.tgz".format(now)
    msg = "web_static packed: {} -> {}Bytes"
    print("Packing web_static to versions/web_static_{}.tgz".format(now))
    if os.path.isdir("versions") is False:
        if local("mkdir -p versions").failed is True:
            return None
    if local("tar -czvf {} web_static".format(archive_path)).failed is True:
        return None
    print(msg.format(archive_path, os.path.getsize(archive_path)))
    return (archive_path)


def do_deploy(archive_path):
    """Deploy the compressed archive to the web servers."""
    if archive_path is None or not os.path.isfile(archive_path):
        return False

    aname = os.path.basename(archive_path)
    rname = aname.split(".")[0]
    vmkdir = "mkdir -p /data/web_static/releases/{}/"
    vtar = "tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
    vrm = "rm /tmp/{}"
    vmv = "mv /data/web_static/releases/{}/web_static/* " \
        "/data/web_static/releases/{}/"
    vrm1 = "rm -rf /data/web_static/releases/{}/web_static"
    vrm2 = "rm -rf /data/web_static/current"
    vln = "ln -s /data/web_static/releases/{}/ /data/web_static/current"

    if put(local_path=archive_path, remote_path="/tmp/").failed is True:
        return False
    if run(vmkdir.format(rname)).failed is True:
        return False
    if run(vtar.format(aname, rname)).failed is True:
        return False
    if run(vrm.format(aname)).failed is True:
        return False
    if run(vmv.format(rname, rname)).failed is True:
        return False
    if run(vrm1.format(rname)).failed is True:
        return False
    if run(vrm2).failed is True:
        return False
    if run(vln.format(rname)).failed is True:
        return False
    print("New version deployed!")
    return True


def deploy():
    """Deploy the latest version of the web_static folder to servers."""
    archive = do_pack()
    if do_deploy(archive):
        return archive
    return False
