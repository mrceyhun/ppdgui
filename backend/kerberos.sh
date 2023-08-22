#!/bin/sh
# Author     : Ceyhun Uzunoglu <ceyhunuzngl AT gmail dot com>

##H Get kerberos ticket using keytab
##H Important : [Works only for KVNO 9 and keytab created using 'cern-get-keytab' script]
##H Usage     : kerberos.sh $keytab
##H Examples  : kerberos.sh /etc/secrets/keytab
##H

# help definition
if [ "$1" = "-h" ] || [ "$1" = "-help" ] || [ "$1" = "--help" ] || [ "$1" = "help" ] || [ "$1" = "" ]; then
    grep "^##H" <"$0" | sed -e "s,##H,,g"
    exit 1
fi

keytab=$1
echo "using keytab=$keytab"

# Current klist -k returns both username@REALM and first.last@REALM as principals, and only "username@REALM" works in our network

# Get realm, see the "@" at the beginning
realm=@$(klist -k "$keytab" | tail -1 | awk -F'@' '{print $2}')

# Get principal which is not "firstname.lastname" but instead "username"
principal=$(klist -k "$keytab" | grep '@' | awk '{print $2}' | awk -F"$realm" '{print $1}' | grep -v '\.' | head -1)

# Principal format is username@REALM
principal="${principal}${realm}"

echo "principal=$principal"
kinit "${principal}" -k -f -p -r 7d -l 7d -t "${keytab}"
exit_status=$?
if [ $exit_status -eq 1 ]; then
    echo "Unable to perform kinit"
    exit 1
fi
echo "Successful kinit"
