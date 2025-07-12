from dataclasses import dataclass
from datetime import datetime, timedelta

from src.stock_history.stock_history import StockHistory

@dataclass
class ShortPositionParameters:

    leverage: int = 2
    quote_qty: float = 200  # QUOTE CURRENCY (USDT)
    max_duration: timedelta = timedelta(hours=2)
    stop_loss: float = 10  # QUOTE CURRENCY (USDT)
    take_profit: float = 10  # QUOTE CURRENCY (USDT)

    def __post_init__(self):
        self.stop_loss = abs(self.stop_loss)  # only positive


@dataclass
class ShortPositionResult:

    pnl: float
    duration: timedelta


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

            if abs(self._pnl) > self._short_position_parameters.stop_loss:
                break

            if abs(self._pnl) > self._short_position_parameters.take_profit:
                break

        self._is_estimated = True

    def get_result(self) -> ShortPositionResult:
        if not self._is_estimated:
            raise Exception('Position is not estimated.')

        return ShortPositionResult(
            pnl=self._pnl,
            duration=self._duration,
        )


class ShortPositionFabric:

    def __init__(
        self,
        short_position_parameters: ShortPositionParameters,
        klines_history: StockHistory,
    ):
        self._short_position_parameters = short_position_parameters
        self._klines_history = klines_history

    def open(self, start_datetime: datetime) -> ShortPosition:

        klines_history = self._klines_history.gt(start_datetime)

        return ShortPosition(
            short_position_parameters=self._short_position_parameters,
            start_datetime=start_datetime,
            klines_history=klines_history,
        )
