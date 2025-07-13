from dataclasses import dataclass
from datetime import timedelta
from typing import Optional


@dataclass(frozen=True)
class ShortPositionParameters:

    leverage: int = 2
    qty: float = 0.02
    # quote_qty: float = 200 # QUOTE CURRENCY (USDT)
    max_duration: timedelta = timedelta(hours=2)
    stop_loss_pnl: Optional[float] = None  # QUOTE CURRENCY (USDT)
    take_profit_pnl: Optional[float] = None  # QUOTE CURRENCY (USDT)
    stop_loss_roi: Optional[float] = None
    take_profit_roi: Optional[float] = None

    def __post_init__(self):
        if self.stop_loss_pnl:
            assert self.stop_loss_pnl == abs(self.stop_loss_pnl)  # only positive
        if self.stop_loss_roi:
            assert self.stop_loss_roi == abs(self.stop_loss_roi)  # only positive

