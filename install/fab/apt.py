from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

SOURCES = '/etc/apt/sources.list'

def configure():
    sudo('dpkg --configure -a')

def update():
    configure()
    sudo('apt-get update -y')

def distupgrade():
    sudo('apt-get dist-upgrade -y')

def upgrade():
    sudo('apt-get upgrade -y')

def add_deb(deb):
    if not files.contains(SOURCES,deb):
        files.append(SOURCES,deb)

def add_key(key):
    sudo('apt-key adv --keyserver keyserver.ubuntu.com --recv %s'%key)

def install(pkg):
    sudo('apt-get install -y --force-yes %s'%pkg)
    #sudo('apt-get install -y %s'%pkg)

