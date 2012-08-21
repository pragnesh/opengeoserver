
#!/usr/bin/python
# -*- coding: utf-8

from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

BY_LABEL = '/dev/disk/by-label/%s'
FSTAB = '/etc/fstab'
MOUNTS = '/proc/mounts'


def vg_create(vg,pv):
     if not files.exists('/dev/{0}'.format(vg)):
        sudo('vgcreate {0} {1}'.format(vg,pv))

def lv_create(vg,lv,size):
    if not files.exists('/dev/{0}/{1}'.format(vg,lv)):
        sudo('lvcreate -L {2} -n {1} /dev/{0}'.format(vg,lv,size))

def xfs_create(vg,lv,size,mp,blksize=4096):
    lv_create(vg,lv,size)

    if not files.exists(mp):
        sudo('mkdir -p {0}'.format(mp))

    if not files.exists(BY_LABEL%lv):
        sudo('mkfs.xfs -f -l size=128m,lazy-count=1 -L {1} -b size={2} /dev/{0}/{1}'.format(vg,lv,blksize))
        #sudo('mkfs.xfs -f -l lazy-count=1 -L {1} -b size={2} /dev/{0}/{1}'.format(vg,lv,blksize))
    if not files.contains(FSTAB,mp):
        files.append(FSTAB,'/dev/{0}/{1} {2}  xfs  logbufs=8,logbsize=256k,osyncisosync,nobarrier,largeio,noatime,nodiratime,inode64,allocsize=512m 0 0'.format(vg,lv,mp))
    if not files.contains(MOUNTS,mp):
        sudo('mount {0}'.format(mp))

#sudo('mount -t xfs -o logbufs=8,logbsize=256k,osyncisosync,nobarrier,largeio,noatime,nodiratime,inode64,allocsize=512m /dev/dvg/test /opt')

