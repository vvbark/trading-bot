from datetime import datetime

from src.stock_history.stock_history import StockHistory


class ShortPosition:

    def __init__(
        self,
        leverage: int,
        timestamp: datetime,
        duration: int,
        stock_history: StockHistory,
    ):
        self._leverage = leverage
        self._timestamp = timestamp
        self._duration = duration
        self._stock_history = stock_history

    def calculate_target(self) -> int:
        return 0


class ShortPositionFabric:

    def __init__(
        self,
        leverage: int,
        duration: int,
        stock_history: StockHistory,
    ):
        self._leverage = leverage
        self._duration = duration
        self._stock_history = stock_history

    def open(self, timestamp: datetime) -> ShortPosition:

        stock_history = self._stock_history.gt(timestamp)

        return ShortPosition(
            leverage=self._leverage,
            timestamp=timestamp,
            duration=self._duration,
            stock_history=self._stock_history,
        )
