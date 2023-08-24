# ppdgui

CMS PPD Physics Run Monitoring

Main Endpoint: http://ceyhun-k8s-lbva4duqns2g-node-0:32000 // accessible only in CERN network

### How frontend works

- You have to provide root file name and object directory of that root file in the input bars:
- *Example*:
    - Go to: http://ceyhun-k8s-lbva4duqns2g-node-0:32000
    - **ROOT File EOS
      Path** : `/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/SpecialHLTPhysics15/0003667xx/DQM_V0001_R000366713__SpecialHLTPhysics15__Run2023B-PromptReco-v1__DQMIO.root`
    - **TDirectory Path Inside ROOT File** :`DQMData/Run 366713/EcalPreshower/Run summary/ESRecoSummary`
    - Hit `Show` button and see 5 histograms which are directly read from EOS and their JSONs are rendered using JSROOT.

### How backend works

- Pretty basic FastAPI, PyROOT and tests. Reads root file and returns JSONs (bit complicated than that :blush: ).
- We use mounted `/eos` in k8s so we can access CERN wide accessible EOS directories with proper kerberos
  authentication.
- ROOT files are read directly from EOS and histograms return with their JSON representation to the frontend.
- All the heavy work is carried on backend side and only JSON results send as responses.

### Repository structure

- **backend**:  FastAPI, PyROOT, tests, its Dockerfile
- **frontend**:  Vue.js, Vite(just for vue deployment and build), tailwind CSS, JSROOT, its Dockerfile
- **kubernetes**:  ppdgui.yaml Kubernetes manifest file for both Frontend and Backend deployment
- **.github/workflows**: CI, GitHub actions that automatically builds docker images of both frontend and backend, and pushes to docker registry:
    - https://hub.docker.com/repository/docker/mrceyhun/ppdgui-front
    - https://hub.docker.com/repository/docker/mrceyhun/ppdgui-back



## Kubernetes

### Backend container details

- We could not solve `kinit -k -t keytab $principle`, preauthentication fails but `kinit $principle` works. Still
  debugging. Probably it's lack of a library, but I could not find it in ubuntu.
- We provide config.yaml in configMap which includes backend server details.
- Cron is to update kerberos ticket automatically however keytab problem prevent to use it.
- Currently, it's running with manual kinit and background job `python backend/main.py >>/proc/1/fd/1 2>&1 &`.
- SwaggerUI can be accessible in http://ceyhun-k8s-lbva4duqns2g-node-0:32001/docs

### Frontend container details

- Normally, it is not advised to run both front/back ends in the same pod. However, this is just for test.
- One workaround is to provide backend API base url to the frontend service in run time.
    - We provide backend base url to `axios` so we don't define it in each axios request.
    - It is provided in `frontend/src/main.js`
    - We cannot use vite env variable feature of https://vitejs.dev/guide/env-and-mode.html because we build our service
      and run nginx.
    - So, we use a custom solution after build to replace env variable name with `sed`
      in `substitute_environment_variables.sh` before running `nginx`.

## Internal documentations

- [kubernetes/README.md](kubernetes/README.md)
- [frontend/README.md](frontend/README.md)
