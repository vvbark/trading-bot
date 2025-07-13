from dataclasses import dataclass
from datetime import timedelta, datetime

from src.training.position.parameters import ShortPositionParameters


@dataclass(frozen=True)
class ShortPositionResult:

    pnl: float
    duration: timedelta
    start_datetime: datetime
    target: int
    margin: float
    roi: float
    entry_price: float
    buying_commission: float
    selling_commission: float
    input_parameters: ShortPositionParameters
