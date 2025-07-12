import zipfile
from pathlib import Path

import requests

from datetime import date

from src.training.enums import Currency, Timestamp


def _get_date(report_date: date) -> str:
    return report_date.strftime("%Y-%m-%d")


class VisionBinanceExtractor:

    _base_url = "https://data.binance.vision/data/"
    _zip_path_template = "spot/daily/klines/{currency}/{timestamp}/{currency}-{timestamp}-{report_date}.zip"
    _save_path_template = "data/spot/daily/klines/{currency}/{timestamp}/{currency}-{timestamp}-{report_date}.zip"

    def __init__(
        self,
        currency: Currency,
        timestamp: Timestamp,
    ):
        self._zip_path = self._zip_path_template.format(
            currency=currency.value,
            timestamp=timestamp.value,
            report_date="{report_date}",
        )
        self._save_path = self._save_path_template.format(
            currency=currency.value,
            timestamp=timestamp.value,
            report_date="{report_date}",
        )


    def _create_folder(self, report_date: date):
        file_path = Path(self._save_path.format(report_date=_get_date(report_date)))
        file_path.parent.mkdir(parents=True, exist_ok=True)

    def download_file(self, report_date: date) -> str:

        response = requests.get(
            self._base_url + self._zip_path.format(report_date=_get_date(report_date)),
            stream=True,
        )
        response.raise_for_status()  # Will raise an error if download fails

        self._create_folder(report_date)

        path = self._save_path.format(report_date=_get_date(report_date))

        with open(path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return path

    def unzip_file(self, report_date: date) -> str:

        zip_path = Path(self._save_path.format(report_date=_get_date(report_date)))
        extract_to = zip_path.parent

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
            csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]

        if not csv_files:
            raise ValueError(f"No CSV file found in ZIP: {zip_path.name}")

        csv_path = extract_to / csv_files[0]
        return str(csv_path)
