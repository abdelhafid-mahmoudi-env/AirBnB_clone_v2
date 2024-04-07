#!/usr/bin/python3
""" Fabric script that creates and distributes an archive. """
from fabric.api import *
from fabric.operations import run, put, sudo, local
from datetime import datetime
import os


env.hosts = ['52.23.177.252', '18.204.7.7']

env.user = "ubuntu"


def do_pack():
    """generates a .tgz archine from contents of web_static"""
    now = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = "versions/web_static_{}.tgz".format(now)
    try:
        local("mkdir -p ./versions")
        local("tar -cvzf {} web_static"
              .format(filename))
        return filename
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
        using fabric to distribute archive
    """
    if os.path.isfile(archive_path) is False:
        return False
    try:
        archive = archive_path.split("/")[-1]
        path = "/data/web_static/releases"
        put("{}".format(archive_path), "/tmp/{}".format(archive))
        folder = archive.split(".")
        run("mkdir -p {}/{}/".format(path, folder[0]))
        new_archive = '.'.join(folder)
        run("tar -xzf /tmp/{} -C {}/{}/"
            .format(new_archive, path, folder[0]))
        run("rm /tmp/{}".format(archive))
        run("mv {}/{}/web_static/* {}/{}/"
            .format(path, folder[0], path, folder[0]))
        run("rm -rf {}/{}/web_static".format(path, folder[0]))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/{} /data/web_static/current"
            .format(path, folder[0]))
        return True
    except Exception as e:
        return False


def deploy():
    """
        deploy function that creates/distributes an archive
    """
    global package
    if package is None:
        package = do_pack()
    if package is None:
        return False
    return do_deploy(package)
