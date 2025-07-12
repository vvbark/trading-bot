from dataclasses import dataclass
from datetime import datetime

from src.training.enums import Timestamp, Currency

@dataclass(frozen=True)
class DataExtractionConfig:

    CURRENCY = Currency.BTCUSDT
    TIMESTAMP = Timestamp.timestamp_3m
    START_DATE = datetime(2025, 7, 1)
    END_DATE = datetime(2025, 7, 10)

    START_DATE_READ = datetime(2025, 7, 2)
    END_DATE_READ = datetime(2025, 7, 9)
