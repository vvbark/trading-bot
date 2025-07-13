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
        self._parameters = short_position_parameters
        self._start_datetime = start_datetime
        self._klines_history = klines_history

        self.pnl_logging = []
        self.close_datetime_logging = []

        # Additional calculations
        self._entry_price = self._klines_history.get_start_price()
        self._margin = self._entry_price * self._parameters.qty / self._parameters.leverage

        self._duration = timedelta()
        self._pnl = 0

        self._selling_commission = 0
        self._buying_commission = 0

        self._is_estimated = False

    def _update_commission(self, selling_price: float, final_price: float):
        self._selling_commission = selling_price * self._parameters.qty * self._parameters.commission
        self._buying_commission = final_price * self._parameters.qty * self._parameters.commission

    def estimate(self):
        """Calculate short position result.

        P&L = (Entry Price - Current Price) × Quantity.
        """
        if self._is_estimated:
            raise Exception('Position is already closed.')

        stock_history_sample = self._klines_history.pop_row()
        while self._duration < self._parameters.max_duration:

            self._duration = stock_history_sample.close_datetime - self._start_datetime
            self._pnl = (self._entry_price - stock_history_sample.price) * self._parameters.qty

            self.pnl_logging.append(self._pnl)
            self.close_datetime_logging.append(stock_history_sample.close_datetime)

            stock_history_sample = self._klines_history.pop_row()

            if self._check_stop():
                break

        self._update_commission(self._entry_price, stock_history_sample.price)
        self._is_estimated = True

        del self._klines_history  # clear data

    def _check_stop(self) -> bool:

        if self._parameters.stop_loss_pnl:
            if self._pnl <= - self._parameters.stop_loss_pnl:
                return True

        if self._parameters.take_profit_pnl:
            if self._pnl >= self._parameters.take_profit_pnl:
                return True

        if self._parameters.stop_loss_roi:
            if self._pnl <= - self._parameters.stop_loss_roi * self._margin:
                return True

        if self._parameters.take_profit_roi:
            if self._pnl >= self._parameters.take_profit_roi * self._margin:
                return True

        return False

    def _calculate_target(self) -> int:

        if not self._is_estimated:
            raise Exception('Position is not estimated.')

        return int(self._pnl >= self._parameters.take_profit_pnl)

    def get_result(self) -> ShortPositionResult:

        if not self._is_estimated:
            raise Exception('Position is not estimated.')

        return ShortPositionResult(
            pnl=self._pnl,  # without commission
            duration=self._duration,
            start_datetime=self._start_datetime,
            target=self._calculate_target(),
            margin=self._margin,
            roi=self._pnl / self._margin,
            entry_price=self._entry_price,
            buying_commission=self._buying_commission,
            selling_commission=self._selling_commission,
            input_parameters=self._parameters,
        )
