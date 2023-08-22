#!/bin/sh
##H Usage: kerberos.sh $keytab
##H Examples: kerberos.sh /etc/secrets/keytab
##H

# help definition
if [ "$1" = "-h" ] || [ "$1" = "-help" ] || [ "$1" = "--help" ] || [ "$1" = "help" ] || [ "$1" = "" ]; then
    grep "^##H" <"$0" | sed -e "s,##H,,g"
    exit 1
fi

export KRB5CCNAME=/tmp/krb5cc
keytab=$1
echo "using keytab=$keytab"
principal=$(klist -k "$keytab" | tail -1 | awk '{print $2}')
echo "principal=$principal"
kinit "${principal}" -k -f -p -r 7d -l 7d -t "${keytab}"
exit_status=$?
if [ $exit_status -eq 1 ]; then
    echo "Unable to perform kinit"
    exit 1
fi
echo "Successful kinit"
