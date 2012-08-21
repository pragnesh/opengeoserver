
from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

def add(option):
    if not files.contains('/etc/sysctl.conf',option):
        files.append('/etc/sysctl.conf',option)

def load():
    sudo('sysctl -p')
