### Dataset search solution suggestion:

- Get find results in JSON format and implement fuzzy search on it. Run2023 takes less than 1 minutes to run, so a cron job wuth 5/10mins period should work.
- Run2022 takes ~2mins and it will not be updated so a daily cron should work.
- Sizes are a couple of MBs.
- No need to keep this metadata in a database IMHO, although it is simple with lightweight Mongo for instance.


#### Questions:

What is `__ALCAPROMPT.root`, i.e.: `Run2023/StreamALCALumiPixelsCountsExpress/0003657xx/DQM_V0001_R000365753__StreamALCALumiPixelsCountsExpress__Run2023A-PromptCalibProdLumiPCC-Express-v1__ALCAPROMPT.root`?

Is it important to use `DQM_V0001` or `DQM_V0002`?
