from dataclasses import dataclass


@dataclass
class Input:

    datasetId: int
    highValue: float
    lowValue: float
    midValue: float
    name: str
    unit: str
    warmingScenario: str
    longitude: str
    latitude: str

