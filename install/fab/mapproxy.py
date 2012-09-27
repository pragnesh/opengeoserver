from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

def pip_mapproxy(path,purge=False,url='https://github.com/mapproxy/mapproxy/tarball/1.4.x'):
    if not files.contains('/usr/share/proj/epsg','<900913>'):
        files.append('/usr/share/proj/epsg','<900913> +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs +over<>')

    if purge:
        sudo('rm -rf %s'%path)

    if not files.exists(path):
        sudo('virtualenv --distribute --system-site-packages %s'%path)
        sudo('. %s/bin/activate && pip install -U %s'%(path,url))
        sudo('. %s/bin/activate && pip install -U eventlet'%path)
        sudo('. %s/bin/activate && pip install -U gunicorn'%path)
        sudo('. %s/bin/activate && pip install -U Shapely'%path)


def mapnik_config():
    local('rsync -avSP --delete ./config/mapnik {0}@{1}:/opt'.format(env.user,env.host))
    sudo('chown -R mapbox /opt/mapnik')

def mapproxy_config():
    mapnik_config()
    mapproxy_config_nginx()
    mapproxy_config_public()
    mapproxy_config_anim()
    mapproxy_config_test()
    mapproxy_config_qs()
    mapproxy_config_demo()
    mapproxy_config_wms()



def mapproxy_config_nginx():

    put('./config/mapproxy/nginx/mapproxy','/etc/nginx/sites-available')
    sudo('ln -sf /etc/nginx/sites-available/mapproxy /etc/nginx/sites-enabled')
    sudo('chown -R mapbox /opt/mapproxy')
    sudo('chown -R mapbox /opt/cache')
    sudo('service nginx restart')

def mapproxy_config_public():
    path_virtenv = '/opt/pyenv/mapproxy/public'
    path_config = '/opt/mapproxy/public'
    pip_mapproxy(path_virtenv)
    #pip_mapproxy(path_virtenv,purge=True,url="https://github.com/mapproxy/mapproxy/tarball/master")
    #sudo('rm -rf /opt/cache/prod')
    if files.exists(path_config):
        sudo ('rm -rf %s'%path_config)
    sudo('mkdir -p %s'%path_config)
    #sudo('. %s/bin/activate && mapproxy-util create --force -t base-config %s'%(path_virtenv,path_config))
    put('config/mapproxy/public/*.yaml','%s'%path_config)
    sudo('. %s/bin/activate && cd %s && mapproxy-util create --force -t wsgi-app -f mapproxy_public.yaml config.py'%(path_virtenv,path_config))
    sudo('chown -R mapbox %s'%path_config)

    put('./config/mapproxy/supervisor/mapproxypublic.conf','/etc/supervisor/conf.d')
    sudo('supervisorctl reload')

def mapproxy_seed_public():
    cmd = """
    sudo su mapbox -
    . /opt/pyenv/mapproxy/public/bin/activate
    cd /opt/mapproxy/public
    mapproxy-seed -s seed_prod.yaml -f mapproxy_public.yaml -c 8
    """

def mapproxy_config_anim():
    path_virtenv = '/opt/pyenv/mapproxy/anim'
    path_config = '/opt/mapproxy/anim'
    pip_mapproxy(path_virtenv)
    if files.exists(path_config):
        sudo ('rm -rf %s'%path_config)
    sudo ('mkdir -p /opt/mapproxy')
    #sudo('. %s/bin/activate && mapproxy-util create --force -t base-config %s'%(path_virtenv,path_config))
    sudo('mkdir -p %s'%path_config)
    put('config/mapproxy/anim/*.yaml','%s'%path_config)
    sudo('. %s/bin/activate && cd %s && mapproxy-util create --force -t wsgi-app -f mapproxy_anim.yaml config.py'%(path_virtenv,path_config))
    sudo('chown -R mapbox %s'%path_config)

    put('./config/mapproxy/supervisor/mapproxyanim.conf','/etc/supervisor/conf.d')
    sudo('supervisorctl reload')


def mapproxy_config_wms():
    path_virtenv = '/opt/pyenv/mapproxy/wms'
    path_config = '/opt/mapproxy/wms'
    pip_mapproxy(path_virtenv)
    if files.exists(path_config):
        sudo ('rm -rf %s'%path_config)
    sudo ('mkdir -p /opt/mapproxy')
    #sudo('. %s/bin/activate && mapproxy-util create --force -t base-config %s'%(path_virtenv,path_config))
    sudo('mkdir -p %s'%path_config)
    put('config/mapproxy/wms/*.yaml','%s'%path_config)
    sudo('. %s/bin/activate && cd %s && mapproxy-util create --force -t wsgi-app -f mapproxywms.yaml config.py'%(path_virtenv,path_config))
    sudo('chown -R mapbox %s'%path_config)

    put('./config/mapproxy/supervisor/mapproxywms.conf','/etc/supervisor/conf.d')
    sudo('supervisorctl reload')

def mapproxy_config_test():
    path_virtenv = '/opt/pyenv/mapproxy/test'
    path_config = '/opt/mapproxy/test'
    sudo ('rm -rf /opt/cache/test')
    pip_mapproxy(path_virtenv,purge=False,url="https://github.com/mapproxy/mapproxy/tarball/master")
    if files.exists(path_config):
        sudo ('rm -rf %s'%path_config)
    sudo ('mkdir -p /opt/mapproxy')
    sudo('. %s/bin/activate && mapproxy-util create --force -t base-config %s'%(path_virtenv,path_config))
    put('config/mapproxy/test/*.yaml','%s'%path_config)
    sudo('. %s/bin/activate && cd %s && mapproxy-util create --force -t wsgi-app -f mapproxy.yaml config.py'%(path_virtenv,path_config))
    sudo('chown -R mapbox %s'%path_config)

    put('./config/mapproxy/supervisor/mapproxytest.conf','/etc/supervisor/conf.d')
    sudo('supervisorctl reload')

def mapproxy_config_qs():
    path_virtenv = '/opt/pyenv/mapproxy/qs'
    path_config = '/opt/mapproxy/qs'
    pip_mapproxy(path_virtenv)
    if files.exists(path_config):
        sudo ('rm -rf %s'%path_config)
    sudo ('mkdir -p /opt/mapproxy')
    #sudo('. %s/bin/activate && mapproxy-util create --force -t base-config %s'%(path_virtenv,path_config))
    sudo('mkdir -p %s'%path_config)
    put('config/mapproxy/qs/*.yaml','%s'%path_config)
    sudo('. %s/bin/activate && cd %s && mapproxy-util create --force -t wsgi-app -f mapproxyqs.yaml config.py'%(path_virtenv,path_config))
    sudo('chown -R mapbox %s'%path_config)

    put('./config/mapproxy/supervisor/mapproxyqs.conf','/etc/supervisor/conf.d')
    sudo('supervisorctl reload')

def mapproxy_config_demo():
    path_virtenv = '/opt/pyenv/mapproxy/demo'
    path_config = '/opt/mapproxy/demo'
    #sudo ('rm -rf /opt/cache/demo')
    #pip_mapproxy(path_virtenv,purge=True,url='https://github.com/mapproxy/mapproxy/tarball/master')
    pip_mapproxy(path_virtenv)
    if files.exists(path_config):
        sudo ('rm -rf %s'%path_config)
    sudo ('mkdir -p /opt/mapproxy')
    sudo('. %s/bin/activate && mapproxy-util create --force -t base-config %s'%(path_virtenv,path_config))
    put('config/mapproxy/demo/*.yaml','%s'%path_config)
    sudo('. %s/bin/activate && cd %s && mapproxy-util create --force -t wsgi-app -f mapproxy.yaml config.py'%(path_virtenv,path_config))
    sudo('chown -R mapbox %s'%path_config)

    put('./config/mapproxy/supervisor/mapproxydemo.conf','/etc/supervisor/conf.d')
    sudo('supervisorctl reload')
