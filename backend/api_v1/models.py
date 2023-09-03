from pydantic import BaseModel


class RequestHistograms(BaseModel):
    """Post request schema to get ROOT object JSON"""
    run_year: int | None = None  # Histograms of a run year, None means recent year
    run_number: int | None = None  # Histograms of a run number, None means recent run


class ResponseHistogram(BaseModel):
    """Representation of histogram"""
    name: str | None = None  # Histogram name
    type: str | None = None  # Histogram type
    data: str | None = None  # JSON


class ResponseDetectorGroup(BaseModel):
    """Representation of histogram"""
    gname: str | None = None  # Detector group name: L1T, HLT
    dataset: str | None = None  # Detector group data root file's dataset name
    root_file: str | None = None  # Detector group root file full EOS path
    histograms: list[ResponseHistogram] | list = []  # Histogram data of the detector group


class ResponseHistograms(BaseModel):
    """Main response schema to histograms requests"""
    run_year: int | None = None  # Run year
    run_number: int | None = None  # Run number
    groups: list[ResponseDetectorGroup] | list = []  # Histogram detector groups list
