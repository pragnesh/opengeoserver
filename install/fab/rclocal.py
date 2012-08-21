

from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files


def add(option):
    if not files.contains('/etc/rc.local',option):
        files.append('/etc/rc.local',option)

def load():
    files.comment('/etc/rc.local','exit 0')
    sudo('. /etc/rc.local')
    files.append('/etc/rc.local','exit 0')

