
from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files


def installimage():
    put('./config/installimage/installimage.conf','/root/installimage.conf')
    run('/root/.oldroot/nfs/install/installimage -a -c /root/installimage.conf')
    run('reboot')

def parted():
    if not files.exists('/dev/sda4'):
        sudo ('parted /dev/sda mkpart primary 1100GB 100%')
        sudo ('parted /dev/sda toggle 4 raid')
        sudo ('parted /dev/sda print')
    if not files.exists('/dev/sdb4'):
        sudo ('parted /dev/sdb mkpart primary 1100GB 100%')
        sudo ('parted /dev/sdb toggle 4 raid')
        sudo ('parted /dev/sdb print')
