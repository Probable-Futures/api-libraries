from dataclasses import dataclass


@dataclass
class Output:
    """This class is not yet used in the API."""

    datasetId: int
    highValue: float
    lowValue: float
    midValue: float
    name: str
    unit: str
    warmingScenario: str
    longitude: str
    latitude: str

