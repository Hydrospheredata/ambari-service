#!/usr/bin/env python
import os
from resource_management import *

# server configurations
config = Script.get_config()

# e.g. /var/lib/ambari-agent/cache/stacks/HDP/2.5/services/MIST/package
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

mist_dirname = 'mist'
install_dir = '/usr/hdp/current'

mist_host = config['configurations']['mist-config']['mist.server.host']
mist_port = config['configurations']['mist-config']['mist.server.port']

mist_version = config['configurations']['mist-ambari-config']['mist.version']
spark_version = config['configurations']['mist-ambari-config']['spark.version']
setup_view = config['configurations']['mist-ambari-config']['mist.setup.view']
mist_addr = config['configurations']['mist-ambari-config']['mist.host.publicname']
spark_home = config['configurations']['mist-ambari-config']['spark.home']

# params from mist-env
mist_ambari_service = config['configurations']['mist-env']['mist_ambari_service']

mist_user = config['configurations']['mist-env']['mist_user']
mist_group = config['configurations']['mist-env']['mist_group']
mist_log_dir = config['configurations']['mist-env']['mist_log_dir']
mist_pid_dir = config['configurations']['mist-env']['mist_pid_dir']
default_config_file = config['configurations']['mist-env']['default_config_file']
default_routers_file = config['configurations']['mist-env']['default_routers_file']
mist_java_args = config['configurations']['mist-env']['mist_java_args']
mist_pid_file = os.path.join(mist_pid_dir, 'mist.pid')
mist_log_file = os.path.join(mist_log_dir, 'mist-setup.log')


mist_dir = os.path.join(*[install_dir, mist_dirname])
conf_dir = os.path.join(*[install_dir, mist_dirname, 'configs'])

# detect configs
master_configs = config['clusterHostInfo']
java64_home = config['hostLevelParams']['java_home']
ambari_host = str(master_configs['ambari_server_host'][0])
mist_internalhost = str(master_configs['mist_master_hosts'][0])
