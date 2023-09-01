# How to

`$ python -m pytest backend/tests/`

## Refs

- (None of them works perfectly though, need some modifications)
- https://fastapi.tiangolo.com/tutorial/testing/
- https://www.fastapitutorial.com/blog/unit-testing-in-fastapi/
- https://medium.com/@nboyet/testing-routes-in-fastapi-app-made-with-beanie-418a300c185c

## How to create test root file

Test data location:
`test/data/DQMGUI_data/Run2023/HLTPhysics/0001234xx/DQM_V0001_R000123456__HLTPhysics__Test-Dataset-Name__DQMIO.root`

```python
from ROOT import TCanvas, TColor, TGaxis, TH1F, TPad
from ROOT import kBlack, kBlue, kRed, TFile, gDirectory


def createH1():
    h1 = TH1F("h1", ("testHistogramTitle"), 100, -5, 5)
    h1.SetLineColor(kBlue + 1)
    h1.SetLineWidth(2)
    h1.FillRandom("gaus")
    h1.GetYaxis().SetTitleSize(20)
    h1.GetYaxis().SetTitleFont(43)
    h1.GetYaxis().SetTitleOffset(1.55)
    h1.SetStats(0)
    return h1


f = TFile.Open("DQM_V0001_R000123456__HLTPhysics__Test-Dataset-Name__DQMIO.root", "recreate")
subdir = f.mkdir("DQMData").mkdir("Run 123456").mkdir("HLT").mkdir("Run summary").mkdir("JME").mkdir("Jets").mkdir(
    "AK4").mkdir("PF").mkdir("HLT_PFJet260")
h = createH1()
subdir.WriteObject(h, "testHistogram")
f.Save()
```
