
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

def ubuntu_gisppa():
    apt.add_rep('ppa:developmentseed/mapbox')
    apt.add_rep('ppa:sharpie/for-science')
    apt.add_rep('ppa:sharpie/postgis-stable')
    apt.add_rep('ppa:ubuntugis/ubuntugis-unstable')
    apt.update()
    apt.upgrade()

def ubuntu_build_essential():
    apt.install('build-essential linux-headers-`uname -r` libpq-dev libxml2-dev libxslt-dev binutils')

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

def tilemill_config():
    put('config/tilemill/tilemill.config','/etc/tilemill')
    with settings(warn_only=True):
        sudo('service tilemill stop')
    sudo('service tilemill start')

def ubuntu_nginx():
    apt.install('nginx')

def nginx_config():
    put('./config/nginx/*','/etc/nginx')
    sudo ('ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/')
    sudo('mkdir -p /var/www/nginx')
    sudo ('cp -r /usr/share/nginx/www/* /var/www/nginx')
    sudo('chown -R www-data.www-data /var/www/nginx')
    sudo('service nginx restart')

def nginx_config_opengeoserver():
    put('./config/opengeoserver/*','/var/www/nginx')
    sudo('chown -R www-data.www-data /var/www/nginx')


