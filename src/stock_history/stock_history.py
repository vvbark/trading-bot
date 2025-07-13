from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import pandas as pd


@dataclass
class StockHistorySample:

    price: float
    close_datetime: datetime


class StockHistory:

    def __init__(
        self,
        window: Optional[pd.DataFrame] = None,
        needs_preparation: bool = True,
    ):
        self._window = window

        if self._window is not None and needs_preparation:
            self._post_init_preparation()

        if self._window is None:
            self._window = pd.DataFrame()

    def _post_init_preparation(self):
        raise NotImplementedError()

    def get_window(self) -> pd.DataFrame:
        return self._window

    def concat(self, stock_history: 'StockHistory') -> 'StockHistory':
        window = pd.concat([self.get_window(), stock_history.get_window()], axis=0)
        return StockHistory(window)

    def gt(self, start_datetime: datetime) -> 'StockHistory':
        """Filter data gt to timestamp."""
        raise NotImplementedError()

    def get_start_price(self) -> float:
        """Returns the start price of the stock."""
        raise NotImplementedError()

    def pop_row(self) -> StockHistorySample:
        raise NotImplementedError()
