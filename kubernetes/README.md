# Kubernetes

## Backend container details

- We could not solve `kinit -k -t keytab $principle`, preauthentication fails but `kinit $principle` works. Still
  debugging. Probably it's lack of a library, but I could not find it in ubuntu.
- We provide config.yaml in configMap which includes backend server details.
- Cron is to update kerberos ticket automatically however keytab problem prevent to use it.
- Currently, it's running with manual kinit and background job `python backend/main.py >>/proc/1/fd/1 2>&1 &`.
- SwaggerUI can be accessible in http://ceyhun-k8s-lbva4duqns2g-node-0:32001/docs

#### How backend it works

- We use mounted `/eos` so we can access CERN wide accessible EOS directories. ROOT file is written directly from EOS
  and histograms return with their JSON representation to the frontend.
- All the heavy work is carried on backend side and only JSON results send to the requests.

## Frontend container details

- Normally, it is not advised to run both front/back ends in the same pod. However, this is just for test.
- One workaround is to provide backend API base url to the frontend service in run time.
    - We provide backend base url to `axios` so we don't define it in each axios request.
    - It is provided in `frontend/src/main.js`
    - We cannot use vite env variable feature of https://vitejs.dev/guide/env-and-mode.html because we build our service
      and run nginx.
    - So, we use a custom solution after build to replace env variable name with `sed`
      in `substitute_environment_variables.sh` before running `nginx`.

#### How frontend it works

- You have to provide root file name and object directory in that root file:
- Example:
    - Go to: http://ceyhun-k8s-lbva4duqns2g-node-0:32000
    - **ROOT File EOS
      Path** : `/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/SpecialHLTPhysics15/0003667xx/DQM_V0001_R000366713__SpecialHLTPhysics15__Run2023B-PromptReco-v1__DQMIO.root`
    - **TDirectory Path Inside ROOT File** :`DQMData/Run 366713/EcalPreshower/Run summary/ESRecoSummary`
    - Hit `Show` button and see 5 histograms which are directly read from EOS and their JSONs are rendered using JSROOT.

## More internal details

#### ppdgui-secret

It requires valid CERN user keytab to access /eos/cms

- Create keytab

```shell
# run ktutil command
ktutil

# it will give you an interactive prompt where you'll need to put your username
# and provide your password
addent -password -p $USER@CERN.CH -k 1 -e rc4-hmac
addent -password -p foo@bar -k 0 -e rc4-hmac
addent -password -p $USER@CERN.CH -k 1 -e aes256-cts
# Name of the file should be "keytab"
wkt keytab
quit
```

- Create `ppdgui-secrets` k8s secret in default namespace

```kubectl create secret generic ppdgui-secrets --from-file=keytab --dry-run=client -o yaml | kubectl apply -f -```

