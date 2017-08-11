#### Start from scratch
0. Select region in AWS - Ireland
1. Create `m4.large` instance from AMI hadoop-sandbox-2.5-docker using security group: Hadoop
2. `ssh ec2-user@host`
3. Add `-p 2004:2004` to start_sandbox.sh
4. Start docker container with sandbox
```
docker rm -f $(docker ps -aq)
chmod +x start_sandbox.sh
./start_sandbox.sh
```
5. Login to container `docker exec -it $(docker ps -aq) bash`
6. Install Mist+Knox using https://github.com/Hydrospheredata/ambari-service/blob/master/KNOX.md
7. Urls:
    * http://54.171.183.81:2004/ui - direct Mist url
    * http://54.171.183.81:8080 - Ambari UI
    * http://54.171.183.81:8080/#/main/views/HYDROSPHERE_VIEW/0.0.1/INSTANCE_1 - Mist view
    * https://54.171.183.81:8443/gateway/hydrosphere/mist/internal/routers - KNOX gateway 
    * http://54.171.183.81:6080/index.html#!/service/3/policies/0 - Ranger policies for gateway, to restrict mist: 
        * click `Add New Policy`
        * type some `Policy Name`
        * `Knox Topology` - must be `hydrosphere`
        * `Knox Service` - must be mist
