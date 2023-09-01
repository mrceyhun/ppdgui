from pydantic import BaseModel


class RequestRootObj(BaseModel):
    """Post request schema to get ROOT object JSON"""
    file_path: str | None = None  # Root file path
    obj_path: str | None = None  # Histogram or object path inside the root file
    all_hists: bool = False  # Return all histograms in the Directory, no subdirectories of course


class ResponseHistogram(BaseModel):
    """Representation of histogram"""
    name: str | None = None  # Histogram name
    type: str | None = None  # Histogram type
    data: str | None = None  # JSON


class ResponseDetectorGroup(BaseModel):
    """Representation of histogram"""
    group: str | None = None  # Detector group : L1T, HLT
    dataset: str | None = None  # Detector group data root file's dataset name
    root_file: str | None = None  # Detector group root file full EOS path
    histograms: list[ResponseHistogram] | list = []  # Histogram data of the detector group


class ResponseHistograms(BaseModel):
    """Main response schema to histograms requests"""
    run_year: int | None = None  # Run year
    run_number: int | None = None  # Run number
    groups: list[ResponseDetectorGroup] | list = []  # Histogram detector groups list
