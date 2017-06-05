#!/usr/bin/env python

import glob
import os
import pwd
import grp
import sys
import tarfile
import urllib
from resource_management import *

reload(sys)
sys.setdefaultencoding('utf8')


class Master(Script):
    def install(self, env):
        import params
        env.set_params(params)

        Execute('find ' + params.service_packagedir + ' -iname "*.sh" | xargs chmod +x')
        # create the log, pid, mits dirs
        Directory([params.mist_pid_dir, params.mist_log_dir, params.mist_dir, params.conf_dir],
                  owner=params.mist_user,
                  group=params.mist_group
                  )

        self.create_linux_user(params.mist_user, params.mist_group)
        print 'Install the Mist Master'
        File(params.mist_log_file,
             mode=0644,
             owner=params.mist_group,
             group=params.mist_group,
             content=''
             )
        print 'Getting mist'


        urllib.urlretrieve(format("http://repo.hydrosphere.io/static/mist-{mist_version}-{spark_version}.tar.gz"), "/tmp/mist.tar.gz")

        print 'Untar archive'
        tar = tarfile.open("/tmp/mist.tar.gz")
        tar.extractall(path="/tmp")
        tar.close()
        Execute(format("cp -R /tmp/mist-{mist_version}-{spark_version}/* {mist_dir}"))
        Execute(format("sudo chown -R {mist_user}:hadoop {mist_dir}"))

        # Install packages listed in metainfo.xml
        self.install_packages(env)
        self.configure(env)

        print 'Setup view'
        Execute(format("{service_packagedir}/scripts/setup_view.sh {mist_dir} "
                       "{mist_addr} {mist_port} {setup_view} {service_packagedir} "
                       "{java64_home} >> {mist_log_file}"),
                user=params.mist_user)

        mist_ambari_service = InlineTemplate(params.mist_ambari_service)
        File(format("/etc/init.d/mist"), content=mist_ambari_service,
             owner=params.mist_user, group=params.mist_group, mode=0777)
        Execute("sudo /sbin/chkconfig --add mist")
        Execute("sudo /sbin/chkconfig mist on")


        if params.setup_view:
            if params.ambari_host == params.mist_internalhost and not os.path.exists(
                    '/var/lib/ambari-server/resources/views/ambari-proxied-view-0.0.1.jar'):
                Execute('echo "Copying mist view jar to ambari views dir"')
                Execute(format("cp {mist_dir}/ambari-proxied-view-0.0.1.jar "
                               "/var/lib/ambari-server/resources/views"), ignore_failures=True)

    def configure(self, env):
        import params
        import status_params
        env.set_params(params)
        env.set_params(status_params)

        mist_default = InlineTemplate(status_params.mist_default_template_config)
        File(format(params.default_config_file), content=mist_default, owner=params.mist_user, group=params.mist_group, mode=0644)

        mist_routers = InlineTemplate(status_params.mist_routers_template_config)
        File(format(params.default_routers_file), content=mist_routers, owner=params.mist_user, group=params.mist_group, mode=0644)

    def stop(self, env):
        self.configure(env)
        print 'Start the Mist Master'
        Execute ('service mist stop')
    def start(self, env):
        self.configure(env)
        print 'Start the Mist Master'
        Execute ('service mist start')

    def status(self, env):
        import status_params
        env.set_params(status_params)

        pid_file = glob.glob(status_params.mist_pid_file)[0]
        check_process_status(pid_file)
    def create_linux_user(self, user, group):
        try:
            pwd.getpwnam(user)
        except KeyError:
            Execute('adduser ' + user)
        try:
            grp.getgrnam(group)
        except KeyError:
            Execute('groupadd ' + group)


if __name__ == "__main__":
    Master().execute()
