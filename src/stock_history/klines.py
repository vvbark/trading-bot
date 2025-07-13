from datetime import datetime

import pandas as pd

from src.stock_history.stock_history import StockHistory, StockHistorySample


class KLinesStockHistory(StockHistory):

    def _post_init_preparation(self):
        self._window = self._window.sort_values('open_time').reset_index(drop=True)
        self._window['close_datetime'] = pd.to_datetime(self.get_window()['close_time'], unit='us')

    def gt(self, start_datetime: datetime) -> 'StockHistory':
        """Filter data gt to timestamp."""
        window = self._window[
            self._window["close_datetime"] >= start_datetime
            ]

        if window.shape[0] == 0:
            raise Exception()

        return KLinesStockHistory(window, needs_preparation=False)

    def concat(self, stock_history: StockHistory) -> StockHistory:
        window = pd.concat([self.get_window(), stock_history.get_window()], axis=0)
        return KLinesStockHistory(window)

    def get_start_price(self) -> float:
        return self._window['close'].iloc[0]

    def pop_row(self) -> StockHistorySample:

        row = self._window.iloc[0]
        self._window = self._window.iloc[1:]

        if self._window.shape[0] == 0:
            raise Exception('No more stock data.')

        return StockHistorySample(
            price=row['close'],
            close_datetime=row['close_datetime'],
        )
