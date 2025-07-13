from datetime import datetime, timedelta

from src.stock_history.stock_history import StockHistory
from src.training.position.parameters import ShortPositionParameters
from src.training.position.results import ShortPositionResult


class ShortPosition:

    def __init__(
        self,
        short_position_parameters: ShortPositionParameters,
        start_datetime: datetime,
        klines_history: StockHistory,
    ):
        self._short_position_parameters = short_position_parameters
        self._start_datetime = start_datetime
        self._klines_history = klines_history

        # Additional calculations
        self._entry_price = self._klines_history.get_start_price()
        self._qty = (
                self._short_position_parameters.quote_qty
                / self._entry_price
                * self._short_position_parameters.leverage
        )  # Quantity = Quote Quantity / Entry Price * Leverage

        self._duration = timedelta()
        self._pnl = 0

        self._pnl_logging = []
        self._close_datetime_logging = []

        self._is_estimated = False

    def estimate(self):
        """Calculate short position result.

        P&L = (Entry Price - Current Price) × Quantity.
        """
        if self._is_estimated:
            raise Exception('Position is already closed.')

        while self._duration < self._short_position_parameters.max_duration:

            stock_history_sample = self._klines_history.pop_row()
            self._duration = stock_history_sample.close_datetime - self._start_datetime
            self._pnl = (self._entry_price - stock_history_sample.price) * self._qty

            self._pnl_logging.append(self._pnl)
            self._close_datetime_logging.append(stock_history_sample.close_datetime)

            if abs(self._pnl) > self._short_position_parameters.stop_loss:
                break

            if abs(self._pnl) > self._short_position_parameters.take_profit:
                break

        self._is_estimated = True
        del self._klines_history  # clear data

    def get_pnl_logging(self) -> list[float]:
        return self._pnl_logging

    def get_close_datetime_logging(self) -> list[datetime]:
        return self._close_datetime_logging

    def get_result(self) -> ShortPositionResult:
        if not self._is_estimated:
            raise Exception('Position is not estimated.')

        return ShortPositionResult(
            pnl=self._pnl,
            duration=self._duration,
            input_parameters=self._short_position_parameters,
        )
