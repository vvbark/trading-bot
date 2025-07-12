from datetime import datetime
from typing import Optional

import pandas as pd


class StockHistory:

    def __init__(
        self,
        window: Optional[pd.DataFrame] = None,
        needs_preparation: bool = True,
    ):
        self._window = window

        if self._window is None:
            self._window = pd.DataFrame()

        if self._window is None and needs_preparation:
            self._post_init_preparation()

    def _post_init_preparation(self):
        raise NotImplementedError()

    def get_window(self) -> pd.DataFrame:
        return self._window

    def concat(self, stock_history: 'StockHistory') -> 'StockHistory':
        self._window = pd.concat([self.get_window(), stock_history.get_window()], axis=0)
        return self

    def gt(self, timestamp: datetime) -> 'StockHistory':
        """Filter data gt to timestamp."""
        raise NotImplementedError()
