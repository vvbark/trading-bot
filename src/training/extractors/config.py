from dataclasses import dataclass
from datetime import date

from src.training.enums import Timestamp, Currency

@dataclass(frozen=True)
class DataExtractionConfig:

    CURRENCY = Currency.BTCUSDT
    TIMESTAMP = Timestamp.timestamp_1m
    START_DATE = date(2025, 1, 1)
    END_DATE = date(2025, 7, 13)

    START_DATE_READ = date(2025, 1, 1)
    END_DATE_READ = date(2025, 7, 2)
