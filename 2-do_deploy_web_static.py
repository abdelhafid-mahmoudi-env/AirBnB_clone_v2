#!/usr/bin/python3
"""Deploys an archive to web servers."""

from fabric.api import put, run, env
import os

# Set the environment hosts and user for deployment
env.hosts = ["52.23.177.252", "18.204.7.7"]
env.user = "ubuntu"

def do_deploy(archive_path):
    """Deploys archive to servers after validating the path and extension."""
    # Validate the archive path exists and has a .tgz extension
    if not os.path.isfile(archive_path) or not archive_path.endswith('.tgz'):
        return False

    try:
        # Transfer the archive to the remote server
        res = put(archive_path, "/tmp/")
        if not res.succeeded:
            return False

        basename = os.path.basename(archive_path)
        name = basename[:-4]  # Remove .tgz extension
        new_dir = f"/data/web_static/releases/{name}"

        # Execute deployment steps
        run(f"mkdir -p {new_dir}")
        run(f"tar -xzf /tmp/{basename} -C {new_dir}")
        run(f"rm /tmp/{basename}")
        run(f"mv {new_dir}/web_static/* {new_dir}")
        run(f"rm -rf {new_dir}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {new_dir} /data/web_static/current")
    except Exception as e:
        return False
    return True
