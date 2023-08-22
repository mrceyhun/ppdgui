# Kubernetes

#### ppdgui-secret

It requires valid CERN user keytab to access /eos/cms

- Create keytab

```shell
# run ktutil command
ktutil

# it will give you an interactive prompt where you'll need to put your username
# and provide your password
addent -password -p $USER@CERN.CH -k 1 -e rc4-hmac
addent -password -p $USER@CERN.CH -k 1 -e aes256-cts
# Name of the file should be "keytab"
wkt keytab
quit
```

- Create `ppdgui-secrets` k8s secret in default namespace

```kubectl create secret generic ppdgui-secrets --from-file=keytab --dry-run=client -o yaml | kubectl apply -f -```

