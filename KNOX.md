#### Setup service to knox

1. [Install Hydrosphere.io](https://github.com/Hydrospheredata/ambari-service/blob/master/README.md)
2. Check Mist service
```
curl localhost:2004/internal/routers
```
3. Create directory with service
```
mkdir -p /usr/hdp/current/knox-server/data/services/mist/0.0.1/
```
4. Add service definition to knox
```
cat << EOF > /usr/hdp/current/knox-server/data/services/mist/0.0.1/service.xml
<service role="MIST" name="mist" version="0.0.1">
  <routes>
    <route path="/mist/**"/>
  </routes>
</service>
EOF
```
5. Add rewrite definition to knox
```
cat << 'EOF' > /usr/hdp/current/knox-server/data/services/mist/0.0.1/rewrite.xml
<rules>
  <rule dir="IN" name="MIST/mist/inbound" pattern="*://*:*/**/mist/{path=**}?{**}">
    <rewrite template="{$serviceUrl[MIST]}/{path=**}?{**}"/>
  </rule>
</rules>
EOF
```
6. Add hydrosphere topology file to knox 
```
cat <<EOF > /usr/hdp/current/knox-server/conf/topologies/hydrosphere.xml
<topology>
    <gateway>
        <provider>
            <role>authentication</role>
            <name>ShiroProvider</name>
            <enabled>true</enabled>
            <param>
                <name>sessionTimeout</name>
                <value>30</value>
            </param>
            <param>
                <name>main.ldapRealm</name>
                <value>org.apache.hadoop.gateway.shirorealm.KnoxLdapRealm</value>
            </param>
            <param>
                <name>main.ldapRealm.userDnTemplate</name>
                <value>uid={0},ou=people,dc=hadoop,dc=apache,dc=org</value>
            </param>
            <param>
                <name>main.ldapRealm.contextFactory.url</name>
                <value>ldap://sandbox.hortonworks.com:33389</value>
            </param>
            <param>
                <name>main.ldapRealm.contextFactory.authenticationMechanism</name>
                <value>simple</value>
            </param>
            <param>
                <name>urls./**</name>
                <value>authcBasic</value>
            </param>
        </provider>
        <provider>
            <role>identity-assertion</role>
            <name>Default</name>
            <enabled>true</enabled>
        </provider>
        <provider>
            <role>authorization</role>
            <name>XASecurePDPKnox</name>
            <enabled>true</enabled>
        </provider>
    </gateway>
    <service>
        <role>MIST</role>
        <url>http://sandbox.hortonworks.com:2004/</url>
    </service>
</topology>
EOF
```
6. Start Knox in Ambari-UI and turn on Demo LDAP
![Image](screenshots/start_demo_ldap.png?raw=true)
7. Check knox gateway
```
curl -iku guest:guest-password -X GET 'https://sandbox.hortonworks.com:8443/gateway/hydrosphere/mist/internal/routers'
```
8. Got to the Ranger http://sandbox.hortonworks.com:6080/index.html, select Knox.
![Image](screenshots/ranger_knox.png?raw=true)
9. Add New Policy with "Knox Topology"==hydrosphere
![Image](screenshots/ranger_add_policy.png?raw=true)