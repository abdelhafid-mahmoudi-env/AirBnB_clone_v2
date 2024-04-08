#!/usr/bin/python3
"""
deploy a compressed version of a web_static folder to web servers
"""

from fabric.api import put, env, run, local, runs_once
from datetime import datetime
from os.path import isdir, getsize, isfile, basename
env.hosts = ["52.23.177.252", "18.204.7.7"]
env.user = "ubuntu"


@runs_once
def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder."""
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(now)
        msg = "web_static packed: {} -> {}Bytes"
        print("Packing web_static to versions/web_static_{}.tgz".format(now))
        if isdir("versions") is False:
            local("mkdir -p versions")
        local("echo '<html><head></head><body>my_index.html</body></html>' > web_static/my_index.html")
        local("tar -czvf {} web_static".format(archive_path))
        print(msg.format(archive_path, getsize(archive_path)))
        return archive_path
    except Exception:
        return None


def do_deploy(archive_path):
    """Deploy the compressed archive to the web servers."""
    if archive_path is None or not isfile(archive_path):
        return False
    try:
        aname = basename(archive_path)
        rname = aname.split(".")[0]
        vmkdir = "mkdir -p /data/web_static/releases/{}/"
        vtar = "tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
        vrm = "rm /tmp/{}"
        vmv = "mv /data/web_static/releases/{}/web_static/* " \
            "/data/web_static/releases/{}/"
        vrm1 = "rm -rf /data/web_static/releases/{}/web_static"
        vrm2 = "rm -rf /data/web_static/current"
        vln = "ln -s /data/web_static/releases/{}/ /data/web_static/current"
        put(local_path=archive_path, remote_path="/tmp/")
        run(vmkdir.format(rname))
        run(vtar.format(aname, rname))
        run(vrm.format(aname))
        run(vmv.format(rname, rname))
        run(vrm1.format(rname))
        run(vrm2)
        run(vln.format(rname))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Deploy the latest version of the web_static folder to servers."""
    archive = do_pack()
    if archive is None:
        return False
    if not do_deploy(archive):
        return False
    return True
