from dataclasses import dataclass
from datetime import timedelta


@dataclass
class ShortPositionParameters:

    leverage: int = 2
    quote_qty: float = 200  # QUOTE CURRENCY (USDT)
    max_duration: timedelta = timedelta(hours=2)
    stop_loss: float = 10  # QUOTE CURRENCY (USDT)
    take_profit: float = 10  # QUOTE CURRENCY (USDT)

    def __post_init__(self):
        self.stop_loss = abs(self.stop_loss)  # only positive
