#!/usr/bin/env python
import os
from resource_management import *

# server configurations
config = Script.get_config()

# e.g. /var/lib/ambari-agent/cache/stacks/HDP/2.5/services/MIST/package
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

mist_dirname = 'mist'
install_dir = '/usr/share'

mist_host = config['configurations']['hydrosphere-config']['mist.server.host']
mist_port = config['configurations']['hydrosphere-config']['mist.server.port']


repository_url = config['configurations']['hydrosphere-ambari-config']['mist.tar.repository']
mist_version = config['configurations']['hydrosphere-ambari-config']['mist.version']
spark_version = config['configurations']['hydrosphere-ambari-config']['spark.version']
setup_view = config['configurations']['hydrosphere-ambari-config']['mist.setup.view']
mist_addr = config['configurations']['hydrosphere-ambari-config']['mist.host.publicname']
spark_home = config['configurations']['hydrosphere-ambari-config']['spark.home']

# params from mist-env
mist_ambari_service = config['configurations']['hydrosphere-env']['mist_ambari_service']

mist_user = config['configurations']['hydrosphere-env']['mist_user']
mist_group = config['configurations']['hydrosphere-env']['mist_group']
mist_log_dir = config['configurations']['hydrosphere-env']['mist_log_dir']
mist_pid_dir = config['configurations']['hydrosphere-env']['mist_pid_dir']
mist_java_args = config['configurations']['hydrosphere-env']['mist_java_args']
mist_pid_file = os.path.join(mist_pid_dir, 'mist.pid')
mist_log_file = os.path.join(mist_log_dir, 'mist-setup.log')


base_mist_dir = os.path.join(*[install_dir, mist_dirname])
mist_dir = os.path.join(*[install_dir, mist_dirname, mist_version+"_"+spark_version])
conf_dir = os.path.join(*[install_dir, mist_dirname, mist_version+"_"+spark_version, 'configs'])

# detect configs
master_configs = config['clusterHostInfo']
java64_home = config['hostLevelParams']['java_home']
ambari_host = str(master_configs['ambari_server_host'][0])
mist_internalhost = str(master_configs['hydrosphere_master_hosts'][0])
