from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

from fab.ssh import keyreset, keypush
from fab.hetzner import installimage,parted
from fab.mdadm import md_status,md_create,md_tune,md_delete
from fab.fs import vg_config,fs_config
from fab.ubuntu import *
from fab.postgis import *
from fab.mapproxy import *
from fab.data import *


def ping():
    local('ping %s'%env.host)


def restore_fromserver(host='ogdmirror.org'):
    sudo('rsync -avSP {0}:/opt/data /opt'.format(host))
    sudo('rsync -avSP {0}:/usr/share/mapbox/cache /usr/share/mapbox'.format(host))
    sudo('rsync -avSP {0}:/usr/share/mapbox/project /usr/share/mapbox'.format(host))
    sudo('rsync -avSP {0}:/usr/share/mapbox/export /usr/share/mapbox'.format(host))
