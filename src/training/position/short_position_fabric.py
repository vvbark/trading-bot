from datetime import datetime

from src.stock_history.stock_history import StockHistory
from src.training.position.parameters import ShortPositionParameters
from src.training.position.short_position import ShortPosition


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
