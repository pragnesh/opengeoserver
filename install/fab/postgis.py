from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

def postgis_config():
    put ('config/postgresql/*','/etc/postgresql/9.1/main')
    sudo('service postgresql reload')

def postgis_create_db(db):
    sudo("""sudo -u postgres createdb {0}""".format(db))


def postgis_sql(db,sql):
    sudo("""sudo -u postgres psql -d {0} -c "{1}" """.format(db,sql))

def postgis_sqlfile(db,sql):
    sudo("""sudo -u postgres psql -d {0} -f "{1}" """.format(db,sql))

def postgis_drop_db(db):
    postgis_sql('postgres','DROP DATABASE {0};'.format(db))

def postgis_create_template(template='template_postgis',contrib='/usr/share/postgresql/9.1/contrib/postgis-2.0/'):
    with cd ('/tmp'):

        postgis_create_db(template)
        postgis_sql('postgres',"UPDATE pg_database SET datistemplate='true' WHERE datname='%s';")
        postgis_sqlfile(template,contrib+'postgis.sql')
        postgis_sqlfile(template,contrib+'spatial_ref_sys.sql')
        postgis_sqlfile(template,contrib+'rtpostgis.sql')
        postgis_sqlfile(template,contrib+'topology.sql')

        postgis_sql(template,"CREATE EXTENSION hstore;")
        postgis_sql(template,"CREATE EXTENSION btree_gist;")

        postgis_sql(template,"GRANT ALL ON geometry_columns TO PUBLIC;")
        postgis_sql(template,"GRANT ALL ON geography_columns TO PUBLIC;")
        postgis_sql(template,"GRANT ALL ON spatial_ref_sys TO PUBLIC;")



        #sudo("""sudo -u postgres psql -d postgres -c "UPDATE pg_database SET datistemplate='true' WHERE datname='%s';" -U postgres"""%template)
        #sudo("""sudo -u postgres psql -d %s -f /usr/share/postgresql/9.1/contrib/postgis-2.0/postgis.sql -U postgres"""%template)
        #sudo("""sudo -u postgres psql -d %s -f /usr/share/postgresql/9.1/contrib/postgis-2.0/spatial_ref_sys.sql -U postgres"""%template)
        #sudo("""sudo -u postgres psql -d %s -c "CREATE EXTENSION hstore;" -U postgres """%template)
        #sudo("""sudo -u postgres psql -d %s -c "CREATE EXTENSION btree_gist;" -U postgres """%template)
        #sudo("""sudo -u postgres psql -d %s -c "GRANT ALL ON geometry_columns TO PUBLIC;" -U postgres """%template)
        #sudo("""sudo -u postgres psql -d %s -c "GRANT ALL ON geography_columns TO PUBLIC;" -U postgres"""%template)
        #sudo("""sudo -u postgres psql -d %s -c "GRANT ALL ON spatial_ref_sys TO PUBLIC;" -U postgres"""%template)

def postgis_drop_template(template='template_postgis'):
    with cd ('/tmp'):
        postgis_drop_db(template)
