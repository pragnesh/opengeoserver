
from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

from lvm import *

def vg_config():
    #parted()
    #md_create()
    #md_tune()
    vg_create('dvg','/dev/md2')


def fs_config():
    #parted()
    #md_create()
    #md_tune()
    #vg_create('dvg','/dev/md2')
    # vg,lv,mp,size,blksize=4096
    #xfs_create ('dvg','test','1T','/opt/test')
    xfs_create ('dvg','postgresql','200G','/var/lib/postgresql')
    #xfs_create ('dvg','geonode','1G','/var/lib/geonode')
    #xfs_create ('dvg','geoserver','1G','/var/lib/geoserver')
    #xfs_create ('dvg','tomcat','1G','/var/lib/tomcat')
    xfs_create ('dvg','libvirt','100G','/var/lib/libvirt')
    xfs_create ('dvg','log','2G','/var/log')
    xfs_create ('dvg','data','1000G','/opt/data')
    xfs_create ('dvg','cache','400G','/opt/cache')
    xfs_create ('dvg','osm','200G','/opt/osm')
    xfs_create ('dvg','mapbox','200G','/usr/share/mapbox')
    xfs_create ('dvg','mapproxy','2G','/opt/mapproxy')
    xfs_create ('dvg','mapnik','2G','/opt/mapnik')
    xfs_create ('dvg','pyenv','2G','/opt/pyenv')
    xfs_create ('dvg','fonts','2G','/opt/fonts')
    #xfs_create ('dvg','locks','2G','/opt/locks')
