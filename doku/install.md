export host='opengeoserver.at'
export user='root'

fab -u $user -H $host keyreset
fab -u $user -H $host keypush
fab -u $user -H $host installimage

fab -u $user -H $host keyreset
fab -u $user -H $host keypush

fab -u $user -H $host parted
fab -u $user -H $host md_delete
fab -u $user -H $host md_create
fab -u $user -H $host md_tune
fab -u $user -H $host md_status

fab -u $user -H $host vg_config
fab -u $user -H $host fs_config

fab -u $user -H $host ubuntu_basic
fab -u $user -H $host ubuntu_gisppa
fab -u $user -H $host ubuntu_build_essential
fab -u $user -H $host ubuntu_build_geo
fab -u $user -H $host ubuntu_postgis

fab -u $user -H $host ubuntu_python
fab -u $user -H $host ubuntu_geopython
fab -u $user -H $host postgis_config
fab -u $user -H $host postgis_create_template
#fab -u $user -H $host postgis_drop_template

fab -u $user -H $host osm_tools

fab -u $user -H $host ubuntu_tilemill
fab -u $user -H $host tilemill_config

fab -u $user -H $host ubuntu_nginx
fab -u $user -H $host nginx_config
fab -u $user -H $host nginx_config_opengeoserver

fab -u $user -H $host mapnik_config
fab -u $user -H $host pip_mapproxy
fab -u $user -H $host mapproxy_config
fab -u $user -H $host mapproxy_config_public

fab -u $user -H $host restore_fromserver

fab -u $user -H $host osm_data

fab -u $user -H $host ubuntu_backup
fab -u $user -H $host backup_config
fab -u $user -H $host backup_run

#fab ubuntu_tincserver
#fab data_group

fab osm_tools
fab mapnik_config
fab mapproxy
fab mapproxy_config
fab ubuntu_darkstat
fab ubuntu_munin
fab push_fabfile

ssh root@geocloud.at
cd /opt/fab
screen
fab osm_data

sudo su - mapbox
. /opt/pyenv/mapproxy/demo/bin/activate
cd /opt/mapproxy/demo
cd . && mapproxy-util serve-develop mapproxy.yaml -b 0.0.0.0:9210

cd . &&  mapproxy-util grids --list --mapproxy-conf mapproxy.yaml
cd . && mapproxy-util grids --grid epsg3857 --mapproxy-conf mapproxy.yaml
