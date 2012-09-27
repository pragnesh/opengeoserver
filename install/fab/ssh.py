from fabric.api import env,run,local,put,sudo,settings
from fabric.context_managers import cd
from fabric.contrib import files

from socket import gethostbyname, getfqdn


def keyreset():

    known_hosts = "~/.ssh/known_hosts"
    host = env['host']
    fqdn = getfqdn(host)
    ip = gethostbyname(host)

    local('ssh-keygen -f %s -R %s'%(known_hosts,host))
    local('ssh-keygen -f %s -R %s'%(known_hosts,fqdn))
    local('ssh-keygen -f %s -R %s'%(known_hosts,ip))

def keypush():

    put ('./config/root/ssh/*','/root/.ssh')
    run('chmod 600 /root/.ssh/*')

    local('ssh-copy-id %s@%s'%(env.user,env.host))

