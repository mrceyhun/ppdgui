### Dataset search solution suggestion:

- Get tree results in JSON format and implement fuzzy search on it. Run2023 takes less than 1 minutes to run, so a cron job wuth 5/10mins period should work.
- Run2022 takes ~2mins and it will not be updated so a daily cron should work.
- Sizes are a couple of MBs.
- No need to keep this metadata in a database IMHO, although it is simple with lightweight Mongo for instance.


tree command JSON structure is

```
```

```
$ tree -l -i --noreport -J -I '*.dqminfo' /eos/cms/store/group/comm_dqm/DQMGUI_data/Run202*/ -o ~/seinfeld/ppdgui/downloads/tree.json

-l: follow symbolic link like directory
-i: minified json
--noreport: no report of number of files/dirs in the output
-J: as json
-I: ignore pattern

$ ls -lh ~/seinfeld/ppdgui/downloads/*.json
-rw-r--r--. 1 cuzunogl zh  14M Aug 24 16:15 /afs/cern.ch/user/c/cuzunogl/seinfeld/ppdgui/downloads/tree2022.json
-rw-r--r--. 1 cuzunogl zh 4.8M Aug 24 16:18 /afs/cern.ch/user/c/cuzunogl/seinfeld/ppdgui/downloads/tree2023.json

```


#### Questions:

What is `__ALCAPROMPT.root`, i.e.: `Run2023/StreamALCALumiPixelsCountsExpress/0003657xx/DQM_V0001_R000365753__StreamALCALumiPixelsCountsExpress__Run2023A-PromptCalibProdLumiPCC-Express-v1__ALCAPROMPT.root`?

Is it important to use `DQM_V0001` or `DQM_V0002`?
