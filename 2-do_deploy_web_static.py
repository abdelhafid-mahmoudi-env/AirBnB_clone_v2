#!/usr/bin/python3
""" Fabric script that distributes an archive to your web servers. """

from fabric.api import env, put, run
from os.path import exists

env.hosts = ['52.23.177.252', '18.204.7.7']
env.output['stdout'] = True


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        filename = archive_path.split("/")[-1]
        foldername = filename.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(foldername))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(filename, foldername))
        run("rm /tmp/{}".format(filename))
        run("mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(foldername, foldername))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(foldername))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(foldername))
        print("New version deployed!")
        return True
    except Exception as e:
        return False
