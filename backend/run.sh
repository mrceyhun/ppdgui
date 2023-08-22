#!/bin/sh
# Author     : Ceyhun Uzunoglu <ceyhunuzngl AT gmail dot com>

##H Runs backend service
##H File     : run.sh
##H Usage    : run.sh $keytab
##H Examples : run.sh /etc/secrets/keytab
##H Used environment variables:
##H   - WDIR          : defined in dockerfile
##H   - MY_NODE_NAME  : defined in k8s manifest
##H   - FAST_API_CONF : defined in k8s manifest
##H Used files as input:
##H   - backend/config.tmpl.yaml
##H   - backend/kerberos.sh
##H   - backend/main.py
##H   - /etc/secrets/keytab : defined in k8s manifest

# help definition
if [ "$1" = "-h" ] || [ "$1" = "-help" ] || [ "$1" = "--help" ] || [ "$1" = "help" ] || [ "$1" = "" ]; then
    grep "^##H" <"$0" | sed -e "s,##H,,g"
    exit 1
fi

keytab=$1

# Change _MY_NODE_NAME_ with Kubernetes node name: check kubernetes/ppdgui.yaml for env var $MY_NODE_NAME
sed "s/_MY_NODE_NAME_/$MY_NODE_NAME/" backend/config.tmpl.yaml >"$FAST_API_CONF"

# Start CRON for kerberos cron job

# do not put set -e which cause undesired exit of pgrep on not found: exits with 1
pid=$(pgrep --exact 'cron')
if [ -z "${pid}" ]; then
    echo "Cron is not running, starting..."
    . /etc/environment
    cron -f &
    pid=$(cat /var/run/crond.pid)
    echo "Cron is started now and running with pid:${pid}"
fi

# Initial kerberos authentication
backend/kerberos.sh "$keytab" >>/proc/"${pid}"/fd/1 2>&1

# Add daily kerberos ticket update cron job to crontab
export >/etc/environment
(
    crontab -l 2>/dev/null
    echo "00 3 * * * . /etc/environment; $WDIR/backend/kerberos.sh /etc/secrets/keytab $ >>/proc/$(cat /var/run/crond.pid)/fd/1 2>&1"
) | crontab -

# START FastAPI
echo "Happy ending, starting FastAPI..."
python backend/main.py
