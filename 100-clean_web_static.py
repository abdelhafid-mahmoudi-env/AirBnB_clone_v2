#!/usr/bin/python3
"""Fabric script to delete out-of-date archives."""

from fabric.api import *
import os

env.hosts = ['xx-web-01', 'xx-web-02']
env.user = 'ubuntu'

def do_clean(number=0):
    """Deletes out-of-date archives."""
    number = int(number)
    if number == 0:
        number = 1

    # Cleaning local archives
    local("ls -t versions/web_static_*.tgz | tail -n +{} | xargs rm -f".format(number + 1))

    # Cleaning remote archives
    run("ls -t /data/web_static/releases/web_static_* | tail -n +{} | xargs rm -rf".format(number + 1))

if __name__ == "__main__":
    do_clean()
