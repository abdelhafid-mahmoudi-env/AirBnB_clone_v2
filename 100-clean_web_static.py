#!/usr/bin/python3
"""
Script for automated cleanup of obsolete archives,
utilizing the do_clean function
"""
from fabric.api import *
from datetime import datetime
import os

env.hosts = ['52.23.177.252', '18.204.7.7']
env.user = 'ubuntu'


def deploy():
    """ Deploys the latest archive to the web server """
    archive = do_pack()
    if not archive:
        return False
    return do_deploy(archive)


def do_pack():
    """
    Generates a .tgz archive from the contents
    of the web_static folder
    """
    try:
        local('mkdir -p versions')
        now = '%Y%m%d%H%M%S'
        archive = 'versions/web_static_{}.tgz'.format(
            datetime.now().strftime(now))
        local('tar -cvzf {} web_static'.format(archive))
        print('web_static packed: {} -> {}'.format(archive,
              os.path.getsize(archive)))
        return archive
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Deploy the specified archive to the web server
    """
    if not os.path.exists(archive_path):
        return False
    fname = archive_path.split('/')[1]
    fpath = '/data/web_static/releases/'
    releasespath = fpath + fname[:-4]
    try:
        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(releasespath))
        run('tar -xzf /tmp/{} -C {}'.format(fname, releasespath))
        run('rm /tmp/{}'.format(fname))
        run('mv {}/web_static/* {}/'.format(releasespath, releasespath))
        run('rm -rf {}/web_static'.format(releasespath))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(releasespath))
        print('New version deployed!')
        return True
    except Exception:
        return False


def do_clean(number=0):
    """
    Removes obsolete archives both locally and remotely
    """
    counter = int(number)
    if counter == 0:
        counter = 2
    else:
        counter += 1

    local('cd versions; ls -t | tail -n +{} | xargs rm -rf'
          .format(counter))
    releasespath = '/data/web_static/releases'
    run('cd {}; ls -t | tail -n +{} | xargs rm -rf'
        .format(releasespath, counter))
