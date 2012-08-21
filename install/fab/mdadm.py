#!/usr/bin/python
# -*- coding: utf-8

from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files
import sysctl
import rclocal
import lvm

def md_status():
    sudo('cat /proc/mdstat')

def md_create():
    if not files.exists('/dev/md2'):
        sudo('mdadm --zero-superblock /dev/sda4 /dev/sdb4')
        #sudo('mdadm --create /dev/md2 --chunk=256K --level=10 -p f2 --verbose --bitmap=internal --raid-devices=2  /dev/sda4 /dev/sdb4')
        #sudo('mdadm --create /dev/md2 --force --chunk=64K --level=0 --verbose --bitmap=internal  --raid-devices=2 /dev/sda4 /dev/sdb4')
        sudo('mdadm --create /dev/md2 --force --chunk=32 --level=0 --verbose  --raid-devices=2 /dev/sda4 /dev/sdb4')
        sudo('mdadm --detail --scan --verbose > /etc/mdadm/mdadm.conf')

def md_tune():
    #sysctl.add('dev.raid.speed_limit_min=10000000000')
    #sysctl.add('dev.raid.speed_limit_max=5000000000000')
    #sysctl.load()
    #rclocal.add('echo 16384 > /sys/block/md2/md/stripe_cache_size ')
    #rclocal.add('blockdev --setra 4096 /dev/sda')
    #rclocal.add('blockdev --setra 4096 /dev/sdb')
    #rclocal.add('blockdev --setra 4096 /dev/md1')
    #rclocal.add('blockdev --setra 4096 /dev/md2')
    #rclocal.add('/sbin/hdparm -S 242 /dev/sda')
    #rclocal.add('/sbin/hdparm -S 242 /dev/sdb')
    #rclocal.load()
    rclocal.add("echo 'deadline' > /sys/block/sda/queue/scheduler")
    rclocal.add("echo 'deadline' > /sys/block/sdb/queue/scheduler")
    rclocal.load()
    #run('blockdev --report')
    #run('/sbin/hdparm -i /dev/sda /dev/sdb')
    #run('/sbin/hdparm -tT /dev/md1 /dev/md2')



def md_delete():
    sudo('mdadm --stop /dev/md2')
    #sudo('mdadm --remove /dev/md2')
    sudo('mdadm --zero-superblock /dev/sda4 /dev/sdb4')
    sudo('mdadm --detail --scan --verbose > /etc/mdadm/mdadm.conf')

def sysbench(dir='/opt/test'):

    sudo("mkdir -p {0}".format(dir))
    with cd(dir):
        run('sysbench --test=fileio --num-threads=128 --file-num=256 --file-total-size=64G  prepare')
        run('sysbench --test=fileio --num-threads=128 --file-num=256 --file-total-size=64G --file-test-mode=seqwr run')
        run('sysbench --test=fileio --num-threads=128 --file-num=256 --file-total-size=64G --file-test-mode=seqrd run')
        run('sysbench --test=fileio --num-threads=128 --file-num=256 --file-total-size=64G --file-test-mode=rndwr run')
        run('sysbench --test=fileio --num-threads=128 --file-num=256 --file-total-size=64G --file-test-mode=rndrd run')
        run('sysbench --test=fileio cleanup')
#http://sysbench.sourceforge.net/docs/#introduction
# sysbench
# apt-get install sysbench
# apt-get install smartmontools
# http://www.cyberciti.biz/tips/monitoring-hard-disk-health-with-smartd-under-linux-or-unix-operating-systems.html
# http://www.cyberciti.biz/tips/linux-find-out-if-harddisk-failing.html

# http://ostatic.com/benchio

# http://blog.tsunanet.net/2011/08/mkfsxfs-raid10-optimal-performance.html
# http://mdsh.com/wiki/Wiki?4KSector%3ARAID1%3ALVM%3AXFS
# https://erikugel.wordpress.com/2010/04/11/setting-up-linux-with-raid-faster-slackware-with-mdadm-and-xfs
# http://www.mythtv.org/wiki/Optimizing_Performance#Optimizing_XFS_on_RAID_Arrays
#  https://greenmang0.wordpress.com/2012/03/26/mongodb-on-ebs-with-raid10-lvm-xfs/
# http://www.microdevsys.com/WordPress/2012/04/02/linux-htpc-home-backup-mdadm-raid6-lvm-xfs-cifs-and-nfs/
# http://www.practicalsysadmin.com/wiki/index.php/XFS_optimisation

# sudo /sbin/vgcreate -s 16M lvm-raid1_md1 /dev/md1
# sudo /sbin/mkfs.xfs -l internal,lazy-count=1 -d agcount=4 -b size=4096 /dev/lvm-raid1_md1/media
# blockdev --setra 4096 /dev/md0
# blockdev --setra 4096 /dev/video_vg/video_lv
#  echo 8192 > /sys/block/md0/md/stripe_cache_size

# mkfs.xfs -d sunit=512, swidth=1024 /dev/md2

#$ mdadm --verbose --create /dev/md0 --level=10 --chunk=256 --raid-devices=4 /dev/sdf1 /dev/sdf2 /dev/sdf3 /dev/sdf4
#$ blockdev --setra 65536 /dev/md0 # [3]
#$ mdadm --detail --scan >> /etc/mdadm/mdadm.conf
# echo "/dev/VOL_GRP_NAME/LOGICAL_VOL_GRP /MOUNT_POINT xfs noatime,noexec,nodiratime 0 0" >> /


#mdadm –create –verbose  /dev/md0 –level=raid6 –chunk=64K –auto=p –raid-devices=6  –spare-devices=0  –bitmap=internal /dev/rsd{a,b,c,d,e,f}

# # mkfs.xfs -l size=64m -d agcount=64 -i attr=2,maxpct=5 -L MBPCBackupx /dev/MBPCStorage/MBPCBackup -f
# mount -t xfs -o logbufs=8,noatime,nodiratime,allocsize=512m /dev/MBPCStorage/MBPCBackup MBPCBackupx/
# mount -t xfs -o noatime,nodiratime /dev/dvg/test /opt

