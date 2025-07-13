from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DataGenerationConfig:

    START_DATE = date(2025, 1, 1)
    END_DATE = date(2025, 7, 1)
