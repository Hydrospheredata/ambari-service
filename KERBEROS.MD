#### Install Kerberos
1. 
```
yum install krb5-server krb5-libs krb5-workstation
```
2. Use the utility kdb5_util to create the Kerberos database.
```
kdb5_util create -s
```
3. Start the KDC server and the KDC admin server.
```
/etc/rc.d/init.d/krb5kdc start
/etc/rc.d/init.d/kadmin start
```
4. Create a KDC admin by creating an admin principal. 
```
kadmin.local -q "addprinc admin/admin"
```
5. Restart kadmin
```
/etc/rc.d/init.d/kadmin restart
```
6. Start kerberos wizard (Principal for KAdmin must be `admin/admin@EXAMPLE.COM`)
![Image](screenshots/kerberos_wizard.png?raw=true)
7. Finish wizard
8. Generate mist principal and keytab
```
kadmin.local -q "addprinc -randkey mist/sandbox.hortonworks.com@EXAMPLE.COM"
kadmin.local -q "xst -k /etc/security/keytabs/mist.keytab mist/sandbox.hortonworks.com@EXAMPLE.COM"
chown mist:hadoop /etc/security/keytabs/mist.keytab
chmod 400 /etc/security/keytabs/mist.keytab
```
9. Add keytab and principal configuration to /usr/share/mist/configs/default.conf
```
  context-defaults.spark-conf = {
    spark.master = "yarn"
    spark.driver.host = sandbox.hortonworks.com
  }

  security {
    enabled = true
    keytab = "/etc/security/keytabs/mist.keytab"
    principal = "mist/sandbox.hortonworks.com@EXAMPLE.COM"
  }
```

