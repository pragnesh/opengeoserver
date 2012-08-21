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

fab -u $user -H $host ubuntu_basic

fab ubuntu_basic
#fab btrfs
fab ubuntu_ppa
fab ubuntu_build
fab ubuntu_postgis
fab ubuntu_geo
fab ubuntu_geopython
#fab ubuntu_geonode
#fab geonode_superuser
#fab geonode_config
fab ubuntu_fabric
fab ubuntu_tincserver
fab ubuntu_tilemill
fab ubuntu_nginx
fab nginx_config
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

