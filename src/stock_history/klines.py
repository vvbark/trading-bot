from datetime import datetime

import pandas as pd

from src.stock_history.stock_history import StockHistory


class KLinesStockHistory(StockHistory):

    def _post_init_preparation(self):
        self._window['close_datetime'] = pd.to_datetime(self.get_window()['close_time'], unit='us')

    def gt(self, timestamp: datetime) -> 'StockHistory':
        """Filter data gt to timestamp."""
        window = self._window[
            self._window["open_datetime"] >= timestamp
        ]
        if window.shape[0] == 0:
            raise Exception()

        return KLinesStockHistory(window, needs_preparation=False)
