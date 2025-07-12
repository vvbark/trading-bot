from datetime import date

import pandas as pd

from src.stock_history.klines import KLinesStockHistory
from src.stock_history.stock_history import StockHistory
from src.training.enums import Currency, Timestamp


def _get_date(report_date: date) -> str:
    return report_date.strftime("%Y-%m-%d")


class KLinesStockHistoryExtractor:

    _filepath_template = "data/spot/daily/klines/{currency}/{timestamp}/{currency}-{timestamp}-{report_date}.csv"
    _columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_volume", "num_trades",
        "taker_base_volume", "taker_quote_volume", "ignore"
    ]

    def __init__(
        self,
        currency: Currency,
        timestamp: Timestamp,
    ):
        self._filepath = self._filepath_template.format(
            currency=currency.value,
            timestamp=timestamp.value,
            report_date="{report_date}",
        )

    def extract_history(self, report_date: date) -> StockHistory:
        window = pd.read_csv(
            filepath_or_buffer=self._filepath.format(report_date=_get_date(report_date)),
            header=None,
        )
        window.columns = self._columns
        return KLinesStockHistory(
            window=window,
        )
