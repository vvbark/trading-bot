from dataclasses import dataclass
from datetime import timedelta


@dataclass
class ShortPositionResult:

    pnl: float
    duration: timedelta
