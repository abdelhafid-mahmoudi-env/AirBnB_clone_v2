#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers using the function do_deploy.
"""

from fabric.api import *
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = 'ubuntu'  # Change to appropriate username
env.key_filename = '/path/to/your/ssh/key.pem'  # Change to appropriate SSH key path


def do_deploy(archive_path):
    """Distributes an archive to your web servers."""
    if not os.path.exists(archive_path):
        return False

    try:
        archive_name = os.path.basename(archive_path)
        archive_no_ext = os.path.splitext(archive_name)[0]

        put(archive_path, "/tmp/")
        run("mkdir -p /data/web_static/releases/{}/".format(archive_no_ext))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/"
            .format(archive_name, archive_no_ext))
        run("rm /tmp/{}".format(archive_name))
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
            .format(archive_no_ext, archive_no_ext))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_no_ext))

        print("New version deployed!")
        return True
    except Exception:
        return False
