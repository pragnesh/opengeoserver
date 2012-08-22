
from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

from postgis import *

POSTGIS_TEMPLATE='template_postgis'
HIGHROAD_SQL='/usr/src/HighRoad/views.pgsql'


def data_group():
    sudo('groupadd -f data')
    sudo('usermod -G data mapbox')
    sudo('usermod -G data www-data')
    sudo('usermod -G tomcat6 www-data')
    sudo('chgrp -R data /opt/data')
    sudo('chmod -R g+rwx /opt/data')

def finished(task):
    if files.exists('.finished.%s'%task):
        return True
    else:
        return False

def clearfinished(task):
    if check_finished(task):
        run('rm .finished.%s'%task)

def setfinished(task):
    run('touch .finished.%s'%task)

def osm_data_clean():
    with cd('/opt/osm'):
        sudo('rm -f *.finished europe.osm.pbf')

PLANET_WGET='wget -c http://download.geofabrik.de/osm/%s'
PLANET_NAME='europe.osm.pbf'

IMPOSM_MAPPING='/usr/src/osm-bright/imposm-mapping.py'

OSM_USER='osm'
OSM_PWD='osm'

def osmconvert(osm_in,bb,osm_out):
    run('osmconvert -v --statistics --drop-brokenrefs {0} -b={1} > {2}'.format(osm_in,bb,osm_out))

def imposm(db,mapping,osm_in):
    if '3857' in db:
        run('imposm --proj=EPSG:3857 -c 8 -d {0} --write --read --optimize --overwrite-cache --deploy-production-tables --remove-backup-tables -m {1} {2}'.format(db,mapping,osm_in))
    elif '4326' in db:
        run('imposm --proj=EPSG:4326 -c 8 -d {0} --write --read --optimize --overwrite-cache --deploy-production-tables --remove-backup-tables -m {1} {2}'.format(db,mapping,osm_in))
    else:
        run('imposm -c 8 -d {0} --write --read --optimize --overwrite-cache --deploy-production-tables --remove-backup-tables -m {1} {2}'.format(db,mapping,osm_in))

HIGHROAD_SQL='/usr/src/HighRoad/views.pgsql'

def osm2pgsql (db,osm_in):
    if '3857' in db:
        run('osm2pgsql -v -C 8192 -E 3857 --create --database {0} --username osm --hstore --hstore-all --multi-geometry  --number-processes 8 {1}'.format(db,osm_in))
    elif '4326' in db:
        run('osm2pgsql -v -C 8192 -E 4326 --create --database {0} --username osm --hstore --hstore-all --multi-geometry  --number-processes 8 {1}'.format(db,osm_in))
    else:
        run('osm2pgsql -v -C 8192 --create --database {0} --username osm --hstore --hstore-all --multi-geometry  --number-processes 8 {1}'.format(db,osm_in))

    run('psql -U {0} -d {1} -f {2}'.format(OSM_USER,db,HIGHROAD_SQL))
    run("""psql -U {0} -d {1} -c'
            CREATE INDEX planet_osm_line_gist    ON planet_osm_line    USING GIST (way GIST_GEOMETRY_OPS);
            CREATE INDEX planet_osm_point_gist    ON planet_osm_point    USING GIST (way GIST_GEOMETRY_OPS);
            CREATE INDEX planet_osm_polygon_gist    ON planet_osm_polygon    USING GIST (way GIST_GEOMETRY_OPS);
            CREATE INDEX planet_osm_roads_gist    ON planet_osm_roads    USING GIST (way GIST_GEOMETRY_OPS);
            CREATE INDEX planet_osm_line_tags    ON planet_osm_line    USING GIN (tags);
            CREATE INDEX planet_osm_point_tags   ON planet_osm_point   USING GIN (tags);
            CREATE INDEX planet_osm_polygon_tags ON planet_osm_polygon USING GIN (tags);
            CREATE INDEX planet_osm_roads_tags   ON planet_osm_roads   USING GIN (tags);
            CREATE INDEX planet_osm_ways_tags   ON planet_osm_roads   USING GIN (tags);
            -- CREATE INDEX planet_osm_rels_tags   ON planet_osm_rels   USING GIN (tags);'""".format(OSM_USER,db))

    run("""psql -U {0} -d {1} -c'VACUUM ANALYSE;'""".format(OSM_USER,db))

def osm_data():
    with cd('/opt/osm'):

        task_planet = PLANET_NAME
        if not finished(task_planet):
            run(PLANET_WGET%PLANET_NAME)
            setfinished(task_planet)

        task_db='osm3857'
        if not finished(task_db):
            # postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            #osm2pgsql (task_db,task_osm)
            imposm (task_db,IMPOSM_MAPPING,PLANET_NAME)
            # osm2pgsql (task_db,task_osm)
            setfinished(task_db)

        task_osm = 'twincity.osm'
        if not finished(task_osm ):
            osmconvert(PLANET_NAME,'16.0,47.6,17.3,48.5',task_osm )
            setfinished(task_osm )

        task_db='osmimptwincity'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            imposm (task_db,IMPOSM_MAPPING,task_osm)
            setfinished(task_db)

        task_db='osmpgtwincity'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            osm2pgsql (task_db,task_osm)
            setfinished(task_db)

        task_db='osm_twincity'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            osm2pgsql (task_db,task_osm)
            setfinished(task_db)

#        task_osm = 'europe_cent.osm'
#        if not finished(task_osm ):
#            osmconvert(PLANET_NAME,'2,41,34.0,60.5',task_osm )
#            setfinished(task_osm )


        task_osm = 'austria_east.osm'
        if not finished(task_osm ):
            osmconvert(PLANET_NAME,'12.5,46.3,18.0,49.3',task_osm )
            setfinished(task_osm )

        task_db='osm4326'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            osm2pgsql (task_db,task_osm)
            setfinished(task_db)

        task_osm = 'vienna.osm'
        if not finished(task_osm):
            osmconvert(PLANET_NAME,'15.0,47.5,17.5,49.0',task_osm )
            setfinished(task_osm)

        task_db='osm3857vienna'
        if not finished(task_db):
            postgis_dropdb(task_db)
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            osm2pgsql (task_db,task_osm)
            imposm (task_db,IMPOSM_MAPPING,task_osm)
            setfinished(task_db)

        task_db='osmbrightvienna'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            imposm (task_db,IMPOSM_MAPPING,task_osm)
            setfinished(task_db)

        task_osm = 'linz.osm'
        if not finished(task_osm):
            osmconvert(PLANET_NAME,'14.15,48.15,14.55,48.45',task_osm )
            setfinished(task_osm)

        task_db='osm3857linz'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            osm2pgsql (task_db,task_osm)
            imposm (task_db,IMPOSM_MAPPING,task_osm)
            setfinished(task_db)

        task_osm = 'berlin.osm'
        if not finished(task_osm):
            osmconvert(PLANET_NAME,'12.5,52.0,14.5,53.0',task_osm )
            setfinished(task_osm)

        task_db='osm3857berlin'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            imposm (task_db,IMPOSM_MAPPING,task_osm)
            setfinished(task_db)

        task_db='osmberlin3857'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            imposm (task_db,IMPOSM_MAPPING,task_osm)
            setfinished(task_db)

        task_osm = 'alps.osm'
        if not finished(task_osm):
            osmconvert(PLANET_NAME,'5.0,45.0,20.0,50.0',task_osm )
            setfinished(task_osm)


        task_osm = 'austria.osm'
        if not finished(task_osm):
            osmconvert(PLANET_NAME,'9.0,45.0,20.5,51.5',task_osm )
            setfinished(task_osm)

        task_db='osm3857austria'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            osm2pgsql (task_db,task_osm)
            imposm (task_db,IMPOSM_MAPPING,task_osm)
            setfinished(task_db)

        task_db='osm4326austria'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            osm2pgsql (task_db,task_osm)
            setfinished(task_db)

        task_osm = 'dach.osm'
        if not finished(task_osm):
            osmconvert(PLANET_NAME,'1.5,43.0,24.0,58.0',task_osm )
            setfinished(task_osm)

        task_db='osm3857dach'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            imposm (task_db,IMPOSM_MAPPING,task_osm)
            setfinished(task_db)


#        task_db='osm3857planet'
#        if not finished(task_db):
#            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
#            imposm (task_db,IMPOSM_MAPPING,PLANET_NAME)
#            setfinished(task_db)



def push_fabfile():
    sudo('mkdir -p /opt/fab')
    put('*.py','/opt/fab')
    put('fab','/opt/fab')

def ogdwien_wfs():
    run ('mkdir -p /opt/data/ogdwien')
    with cd('/opt/data/ogdwien'):
        #task_ogr = 'ogdwien_20120508_4326_json.sqlite'
        #if not finished(task_ogr):
            #if  files.exists(task_ogr):
                #run('rm %s'%task_ogr)
            #run("""ogr2ogr -progress -f 'SQLite' ogdwien_20120508_4326_json.sqlite  -dsco SPATIALITE=YES,FORMAT=SPATIALITE,SPATIAL_INDEX=yes WFS:'http://data.wien.gv.at/daten/wfs?service=WFS&OUTPUTFORMAT=json&srsName=EPSG:4326'""")
            #setfinished(task_ogr)

        #task_ogr = 'ogdwien_20120508_31256_json.sqlite'
        #if not finished(task_ogr):
            #if  files.exists(task_ogr):
                #run('rm %s'%task_ogr)
            #run("""ogr2ogr -progress -f 'SQLite' ogdwien_20120508_31256_json.sqlite  -dsco SPATIALITE=YES,FORMAT=SPATIALITE,SPATIAL_INDEX=yes WFS:'http://data.wien.gv.at/daten/wfs?service=WFS&OUTPUTFORMAT=json&srsName=EPSG:31256'""")
            #setfinished(task_ogr)

        task_db='ogdwien'
        if not finished(task_db):
            postgis_createdb_fromtemplate(task_db,POSTGIS_TEMPLATE,OSM_USER,OSM_PWD)
            run("""export PGCLIENTENCODING='ISO-8859-15'&&ogr2ogr -f PostgreSQL PG:'dbname=%s user=%s password=%s' %s"""%(task_db,OSM_USER,OSM_PWD,task_ogr))
            setfinished(task_db)
