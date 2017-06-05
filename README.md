#### An Ambari Service for Hydrosphere
Ambari service for easily installing and managing Hydrosphere on HDP cluster

##### Setup

- Download HDP 2.5+ sandbox VM image (HDP® 2.6 on Hortonworks Sandbox) from [Hortonworks website](https://hortonworks.com/downloads/#sandbox)
- Import Sandbox_HDP into VMWare/VirtualBox and set the VM memory size to 8GB
- Now start the VM
- After it boots up, find the IP address of the VM and add an entry into your machines hosts file e.g.
```
192.168.191.241 sandbox.hortonworks.com sandbox    
```
- Connect to the VM via SSH (password hadoop) and start Ambari server
```
ssh root@sandbox.hortonworks.com

#or use with VirtualBox
ssh root@localhost -p 2222
```
- To deploy the Hydrosphere service, run below on ambari server
```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/Hydrospheredata/ambari-mist-service.git   /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/HYDROSPHERE
```
- Restart Ambari
```
#on sandbox
service ambari restart

#on non-sandbox
sudo service ambari-server restart

#or reset admin password
ambari-admin-password-reset
```
- Install service using Ambari UI
![Image](screenshots/add_service.png?raw=true)
- Configure package
![Image](screenshots/configure.png?raw=true)
- Configure package
![Image](screenshots/service.png?raw=true)
- Start jobs using Hydrosphere View
![Image](screenshots/view.png?raw=true)