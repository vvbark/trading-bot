from dataclasses import dataclass
from datetime import timedelta, datetime

from src.training.position.parameters import ShortPositionParameters


@dataclass
class ShortPositionResult:

    pnl: float
    duration: timedelta
    start_datetime: datetime
    target: int
    margin: float
    roi: float
    entry_price: float
    input_parameters: ShortPositionParameters
