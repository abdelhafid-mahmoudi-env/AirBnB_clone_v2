#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers.
"""

import os
from fabric.api import run, put, env, local
import datetime

# Update the host IP addresses
env.hosts = ["52.23.177.252","18.204.7.7"]
env.user = "ubuntu"


def do_deploy(archive_path):
    """ deploy package """
    if archive_path is None or not os.path.isfile(archive_path):
        print("Archive path is invalid or does not exist.")
        return False

    try:
        # Extract archive name and release name
        archive_name = os.path.basename(archive_path)
        release_name = archive_name.split(".")[0]

        # Transfer archive to server
        put(local_path=archive_path, remote_path="/tmp/")

        # Create directory for release
        run("mkdir -p /data/web_static/releases/{}".format(release_name))

        # Unpack archive to release directory
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
            .format(archive_name, release_name))

        # Remove archive from /tmp directory
        run("rm /tmp/{}".format(archive_name))

        # Move contents of unpacked directory to current deployment
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/"
            .format(release_name, release_name))

        # Remove redundant web_static directory
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(release_name))

        # Update symbolic link to current deployment
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ \
            /data/web_static/current".format(release_name))

        return True

    except Exception as e:
        print("Exception occurred during deployment:", e)
        return False


def do_pack():
    """ package function """
    try:
        # Create versions directory if it doesn't exist
        if not os.path.isdir("./versions"):
            os.makedirs("./versions")

        # Get current timestamp
        ntime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Create .tgz archive of web_static directory
        local("tar -czf versions/web_static_{}.tgz web_static/*".format(ntime))

        # Return path of created archive
        return "versions/web_static_{}.tgz".format(ntime)

    except Exception as e:
        print("Exception occurred during packaging:", e)
        return None


def deploy():
    """ package && deploy to servers """
    # Pack web_static files
    archive_path = do_pack()

    # Check if packaging was successful
    if archive_path is None:
        return False

    # Deploy packaged files
    return do_deploy(archive_path)
