#### An Ambari Service for Mist
Ambari service for easily installing and managing Mist on HDP cluster



- To deploy the Mist service, run below on ambari server
```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/Hydrospheredata/ambari-mist-service.git   /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/MIST
```

- Restart Ambari
```
#on sandbox
service ambari restart

#on non-sandbox
sudo service ambari-server restart
```
