from pydantic import BaseModel


class DqmRootSingleFileMeta(BaseModel):
    """Representation of DQM GUI EOS root file parsed metadata in stored for easy querying"""
    year: int  # Run year
    run: int  # Run number
    det_group: str  # Detector group name, or workspace in DQMGUI: L1T, L1TEMU, HLT,  Pixel, so on
    dataset: str  # Dataset name embedded in the ROOT file name: Run2023A-PromptReco-v1, Run2023D-Express-v1
    eos_path: str  # full EOS path of the root file


class DqmMetaStore(BaseModel):
    """Main DQM ROOT files metadata format"""
    data: list[DqmRootSingleFileMeta]
