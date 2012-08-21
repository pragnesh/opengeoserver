from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

from fab.ssh import keyreset, keypush
from fab.hetzner import installimage,parted
from fab.mdadm import md_status,md_create,md_tune,md_delete
from fab.fs import vg_config,fs_config
from fab.ubuntu import *
from fab.postgis import *

def ping():
    local('ping %s'%env.host)

