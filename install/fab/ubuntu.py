
from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files
import apt
import sysctl

def ubuntu_basic():
    apt.update()
    apt.upgrade()
    apt.install('btrfs-tools subversion git python-dev curl unzip htop dstat screen \
    sysstat iotop powertop latencytop screen chkconfig python-software-properties vim mercurial curl \
    git-core subversion wget make multitail sysbench')

