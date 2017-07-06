#### Install Kerberos
1. 
```
yum install krb5-server krb5-libs krb5-workstation
```
2. 
```
cat << 'EOF' > /etc/krb5.conf
[libdefaults]
  renew_lifetime = 7d
  forwardable = true
  default_realm = EXAMPLE.COM
  ticket_lifetime = 24h
  dns_lookup_realm = false
  dns_lookup_kdc = false
  default_ccache_name = /tmp/krb5cc_%{uid}
  #default_tgs_enctypes = aes des3-cbc-sha1 rc4 des-cbc-md5
  #default_tkt_enctypes = aes des3-cbc-sha1 rc4 des-cbc-md5

[domain_realm]
  sandbox.hortonworks.com = EXAMPLE.COM
  .sandbox.hortonworks.com = EXAMPLE.COM
[logging]
  default = FILE:/var/log/krb5kdc.log
  admin_server = FILE:/var/log/kadmind.log
  kdc = FILE:/var/log/krb5kdc.log

[realms]
 EXAMPLE.COM = {
   kdc = sandbox.hortonworks.com
   admin_server = sandbox.hortonworks.com
}
EOF
```
3. Use the utility kdb5_util to create the Kerberos database.
```
kdb5_util create -s
```
4. Start the KDC server and the KDC admin server.
```
/etc/rc.d/init.d/krb5kdc start
/etc/rc.d/init.d/kadmin start
```
5. Create a KDC admin by creating an admin principal. 
```
kadmin.local -q "addprinc admin/admin"
```
6. Restart kadmin
```
/etc/rc.d/init.d/kadmin restart
```
7. Start kerberos wizard (Principal for KAdmin must be `admin/admin@EXAMPLE.COM`)
![Image](screenshots/kerberos_wizard.png?raw=true)
8`. Finish wizard
