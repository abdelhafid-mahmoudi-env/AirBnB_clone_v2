#!/usr/bin/python3
"""Fabric script (based on the file 1-pack_web_static.py)"""
import os.path
import time
from fabric.api import *
from fabric.operations import run, put, sudo
from datetime import date


env.hosts = ["52.23.177.252", "18.204.7.7"]

archive = None


def do_pack():
    timestamp = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{:s}.tgz web_static/".format(timestamp))
        return "versions/web_static_{:s}.tgz".format(timestamp)
    except:
        return None


def do_deploy(archive_path):
    """script that distributes archive to web servers"""
    if os.path.isfile(archive_path) is False:
        return False

    put(archive_path, "/tmp/")
    unpack = archive_path.split("/")[-1]
    folder = "/data/web_static/releases/" + unpack.split(".")[0]
    run("sudo mkdir -p {:s}".format(folder))
    run("sudo tar -xzf /tmp/{:s} -C {:s}".format(unpack, folder))
    run("sudo rm /tmp/{:s}".format(unpack))
    run("sudo mv {:s}/web_static/* {:s}/".format(folder, folder))
    run("sudo rm -rf {:s}/web_static".format(folder))
    run("sudo rm -rf /data/web_static/current")
    run("sudo ln -s {:s} /data/web_static/current".format(folder))
    return True


def deploy():
    global archive
    archive = do_pack()
    if archive is None:
        archive = do_pack()
    if archive is None:
        return False
    deploythis = do_deploy(archive)
    return deploythis
