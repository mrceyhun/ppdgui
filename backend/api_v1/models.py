from pydantic import BaseModel


class RequestRootObj(BaseModel):
    """Post request schema to get ROOT object JSON"""
    file_path: str | None = None  # Root file path
    obj_path: str | None = None  # Histogram or object path inside the root file
    all_hists: bool = False  # Return all histograms in the Directory, no subdirectories of course


class HistogramJson(BaseModel):
    """Representation of histogram"""
    name: str | None = None  # Histogram name
    data: dict | None = None  # JSON


class ResponseRootObj(BaseModel):
    """Response request schema to get ROOT object JSON or dirs"""
    dirs: list[str] | None = None  # List of subdirectories
    hist_json: list[HistogramJson] | list = []  # list of histogram JSONs
