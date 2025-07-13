from dataclasses import dataclass
from datetime import timedelta

from src.training.position.parameters import ShortPositionParameters


@dataclass
class ShortPositionResult:

    pnl: float
    duration: timedelta
    input_parameters: ShortPositionParameters
