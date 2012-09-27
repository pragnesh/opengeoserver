
from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files
import apt
import sysctl
import rclocal

from lvm import *

def ubuntu_basic():
    apt.update()
    apt.upgrade()
    apt.install('btrfs-tools subversion git python-dev curl unzip htop dstat screen \
    sysstat iotop powertop latencytop screen chkconfig python-software-properties vim mercurial curl \
    git-core subversion wget make multitail sysbench')

def ubuntu_gisppa():
    apt.add_rep('ppa:developmentseed/mapbox')
    apt.add_rep('ppa:sharpie/for-science')
    apt.add_rep('ppa:sharpie/postgis-stable')
    apt.add_rep('ppa:ubuntugis/ubuntugis-unstable')
    apt.update()
    apt.upgrade()

def ubuntu_build_essential():
    apt.install('build-essential linux-headers-`uname -r` libpq-dev libxml2-dev libxslt-dev binutils')

def ubuntu_backup():
    apt.install('rdiff rdiff-backup rdiff-backup-fs')

def backup_config():
    xfs_create ('rvg','backup','800G','/backup')

def backup_run():
    run('mkdir -p /backup/data')
    run('rdiff-backup -v5 --force --print-statistics --no-eas /opt/data /backup/data')
    run('mkdir -p /backup/mapbox')
    run('rdiff-backup -v5 --force --print-statistics --no-eas /usr/share/mapbox /backup/mapbox')
    run('mkdir -p /backup/mapnik')
    run('rdiff-backup -v5 --force --print-statistics --no-eas /opt/mapnik /backup/mapnik')
    run('mkdir -p /backup/mapproxy')
    run('rdiff-backup -v5 --force --print-statistics --no-eas /opt/mapproxy /backup/mapproxy')


def ubuntu_build_geo():
    apt.install('gdal-bin proj g++ cpp  libxml2 libxml2-dev \
    lzma lzma-dev liblzma-dev libfreetype6 libfreetype6-dev \
    ttf-unifont ttf-dejavu ttf-dejavu-core ttf-dejavu-extra \
    libsqlite3-0 libsqlite3-dev spatialite-bin libspatialite3 libspatialite-dev \
    libgeos-dev libgdal-dev libgeos++-dev libproj-dev libgeos-c1')

def ubuntu_python():
    apt.install('python-pkg-resources python-dev python-virtualenv')
    sudo ('pip install fabric')

def ubuntu_geopython():
    apt.install('python-mapnik python-imaging python-yaml libproj0 python-lxml python-shapely python-mongoengine python-mapnik  mapnik-utils \
    python-pyproj python-scipy python-scientific python-numpy \
    python-psycopg2 python-pyke python-shapely python-pymongo python-gridfs ipython \
    python-netcdf cython python-numexpr python-tables python-rpy2 python-lxml \
    python-cairo-dev python-cairo python-imaging \
    libxslt1.1 libxslt1-dev python-lxml python-pastedeploy python-paste python-pastescript python-webob')
    sudo ('ln -sf /usr/lib/x86_64-linux-gnu/libfreetype.so /usr/lib/')
    sudo ('ln -sf /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/')
    sudo ('ln -sf /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/')
    sudo ('pip install owslib')


def ubuntu_postgis():
    sysctl.add('kernel.sem = 250 32000 100 128')
    sysctl.add('kernel.shmall = 2097152')
    sysctl.add('kernel.shmmax = 6656401410')
    sysctl.add('kernel.shmmni = 4096')
    sysctl.add('fs.file-max = 262140')
    sysctl.load()
    apt.install('postgresql-contrib-9.1 postgresql-9.1-postgis2')

def ubuntu_tilemill():
    apt.install('tilemill')

def ubuntu_munin():
    # http://fak3r.com/2010/10/07/howto-monitor-tomcat-with-monit-and-munin-in-debian/
    #http://serverfault.com/questions/339472/configuring-the-tomcat-plugin-of-munin
    #apt.install('munin munin-node munin-plugins-extra libwww-perl libxml-simple-perl libdbd-pg-perl')
    #apt.install('tomcat6-admin')
    #apt.add_rep('ppa:zeppelinlg/munin')
    #apt.update()
    apt.install('munin munin-node munin-plugins-extra libwww-perl libxml-simple-perl libdbd-pg-perl')
    sudo('pip install PyMunin')
    put('config/munin/nginx/munin','/etc/nginx/sites-available')
    sudo('ln -sf /etc/nginx/sites-available/munin /etc/nginx/sites-enabled/munin')

    #put('config/munin/etc/*','/etc/munin')
    #put('config/munin/plugins/*','/usr/share/munin/plugins')
    #put('config/munin/tomcat/*','/etc/tomcat6')

    #with cd('/usr/share/munin/plugins'):
        #sudo('chmod +x nginx_request')
        #sudo('chmod +x nginx_status')
        #sudo('chmod +x nginx_memory')

    #sudo('ln -sf /usr/share/munin/plugins/nginx_request /etc/munin/plugins/nginx_request')
    #sudo('ln -sf /usr/share/munin/plugins/nginx_status /etc/munin/plugins/nginx_status')
    #sudo('ln -sf /usr/share/munin/plugins/nginx_memory /etc/munin/plugins/nginx_memory')
    #sudo('ln -sf /usr/share/munin/plugins/netstat /etc/munin/plugins/netstat')
    #sudo('ln -sf /usr/share/munin/plugins/tcp /etc/munin/plugins/tcp')

    #sudo('ln -sf /usr/share/munin/plugins/tomcat_access /etc/munin/plugins/tomcat_access')
    #sudo('ln -sf /usr/share/munin/plugins/tomcat_jvm /etc/munin/plugins/tomcat_jvm')
    #sudo('ln -sf /usr/share/munin/plugins/tomcat_threads /etc/munin/plugins/tomcat_threads')
    #sudo('ln -sf /usr/share/munin/plugins/tomcat_volume /etc/munin/plugins/tomcat_volume')

    #sudo('ln -sf /usr/local/lib/python2.7/dist-packages/pymunin/plugins/pgstats.py')


    #sudo ('service tomcat6 restart')

    sudo('service munin-node restart')
    sudo('sudo -u munin munin-cron')

    sudo('service nginx restart')
    #sudo -u munin crontab -e
    #*/5 * * * *     /usr/bin/munin-cron

def ubuntu_darkstat():
    apt.install('darkstat')
    put('config/darkstat/etc/*','/etc/darkstat')
    put('config/darkstat/nginx/*','/etc/nginx/sites-available')
    sudo('ln -sf /etc/nginx/sites-available/darkstat /etc/nginx/sites-enabled/darkstat')
    sudo('service darkstat restart')
    sudo('service nginx reload')

def tilemill_config():
    put('config/tilemill/tilemill.config','/etc/tilemill')
    with settings(warn_only=True):
        sudo('service tilemill stop')
    sudo('service tilemill start')

def ubuntu_nginx():
    apt.install('nginx supervisor')
    sudo('update-rc.d supervisor enable')

def nginx_config():
    put('./config/nginx/etc/*','/etc/nginx')
    sudo ('ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/')
    sudo('mkdir -p /var/www/default')
    put('./config/nginx/www/*','/var/www/default')
    sudo('chown -R www-data.www-data /var/www/default')
    sudo('service nginx restart')

def nginx_config_opengeoserver():
    sudo('mkdir -p /var/www/opengeoserver.at')
    put('./config/opengeoserver/www.at/*','/var/www/opengeoserver.at')
    sudo('mkdir -p /var/www/opengeoserver.org')
    put('./config/opengeoserver/www.org/*','/var/www/opengeoserver.org')

    sudo('chown -R www-data.www-data /var/www/opengeoserver.at')
    sudo('chown -R www-data.www-data /var/www/opengeoserver.org')
    put('./config/opengeoserver/nginx/opengeoserver','/etc/nginx/sites-available')
    sudo('ln -sf /etc/nginx/sites-available/opengeoserver /etc/nginx/sites-enabled')
    sudo('service nginx reload')

def osm_tools():
    apt.install('build-essential python-dev protobuf-compiler \
                      libprotobuf-dev libtokyocabinet-dev python-psycopg2 \
                      libgeos-c1 libgeos-dev python-pip\
                      libpq-dev libbz2-dev libprotobuf-c0 libprotobuf-c0-dev automake ')
    sudo('pip install imposm')
    sudo('mkdir -p /usr/src/osmconvert')
    with cd('/usr/src/osmconvert'):
        run('wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -o osmconvert')
        sudo(' cp osmconvert /usr/bin')
    if  files.exists('/usr/src/osm-bright'):
        sudo('rm -rf /usr/src/osm-bright')
    if  files.exists('/usr/src/osm2pgsql'):
        sudo('rm -rf /usr/src/osm2pgsql')
    if  files.exists('/usr/src/HighRoad'):
        sudo('rm -rf /usr/src/HighRoad')
    with cd('/usr/src'):
        run('git clone  https://github.com/mapbox/osm-bright.git')
        run('svn co http://svn.openstreetmap.org/applications/utils/export/osm2pgsql')
        run('git clone  https://github.com/migurski/HighRoad.git')
    with cd('/usr/src/osm2pgsql'):
        run('./autogen.sh')
        run('./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/ ')
        run('make')
        sudo('make install')

def tc():
    rclocal.add('/sbin/tc qdisc del dev eth0 root')
    rclocal.add('/sbin/tc qdisc add dev eth0 root handle 1: htb')
    rclocal.add('/sbin/tc class add dev eth0 parent 1: classid 1:1 htb rate 8mbit burst 2mb cburst 1mb ceil 1000mbit')
    rclocal.add('/sbin/tc class add dev eth0 parent 1:1 classid 1:5 htb rate 8mbit burst 2mb cburst 1mb ceil 1000mbit prio 1')
    rclocal.add('/sbin/tc class add dev eth0 parent 1:1 classid 1:6 htb rate 2500mbit ceil 1000mbit prio 0')
    rclocal.add('/sbin/tc filter add dev eth0 parent 1:0 prio 1 protocol ip handle 5 fw flowid 1:5')
    rclocal.add('/sbin/tc filter add dev eth0 parent 1:0 prio 0 protocol ip handle 6 fw flowid 1:6')
    rclocal.add('/sbin/iptables -A OUTPUT -t mangle -p tcp --sport 80 -j MARK --set-mark 5')
    rclocal.add('/sbin/iptables -A OUTPUT -t mangle -p tcp --sport 22 -j MARK --set-mark 6')
    rclocal.add('/sbin/iptables -A OUTPUT -t mangle -p tcp --sport 443 -j MARK --set-mark 6')
    rclocal.load('')

