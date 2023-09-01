from pydantic import BaseModel, RootModel


class DqmFileMetadata(BaseModel):
    """Representation of single DQM ROOT file's parsed metadata"""
    year: int  # Run year
    run: int  # Run number
    group_directory: str  # Detector group directory: JetMET1, HLTPhysics, so on
    dataset: str  # Dataset name embedded in the ROOT file name: Run2023A-PromptReco-v1, Run2023D-Express-v1
    root_file: str  # full EOS path of the root file


class DqmMetaStore(RootModel):
    """Main DQM ROOT files metadata format"""
    root: list[DqmFileMetadata]

    def __iter__(self):
        return iter(self.root)

    def __getitem__(self, item):
        return self.root[item]
