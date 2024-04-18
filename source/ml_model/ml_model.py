import numpy as np
import pandas as pd
from pathlib import Path
from sktime.forecasting.arima import ARIMA

import source.db_functions as db_con
import source.logger as log
from source.constants import *

ml_logger = log.app_logger(__name__)

rng = np.random.default_rng()

AR_LOWER = 0.1
AR_UPPER = 0.6
MEAN_LOWER = 1000
MEAN_UPPER = 2000
STD = 1


def generate_integrated_autocorrelated_series(
    p: float, mean: float, std: float, length: int
) -> np.ndarray:
    """Generates an integrated autocorrelated time series
    using a specified autoregression parameter, mean and standard deviation
    of the normal distribution, and the desired length of the series."""
    x = 0
    ar1_series = np.asarray([x := p * x + rng.normal(0, 1) for _ in range(length)])
    return np.cumsum(ar1_series * std) + mean


def generate_sample_data(
    cols: list[str], x_size: int, y_size: int
) -> tuple[pd.DataFrame, pd.DataFrame, tuple[np.ndarray, np.ndarray]]:
    """Generates sample training and test data for specified columns.
    The data consists of autocorrelated series,
    each created with randomly generated autoregression coefficients and means.
    The method also returns the generated autocorrelation coefficients and means for reference.
    'x_size' determines the length of the training set, and 'y_size' determines the length of the test set.
    'cols' determines the names of the columns."""
    ar_coefficients = rng.uniform(AR_LOWER, AR_UPPER, len(cols))
    means = rng.uniform(MEAN_LOWER, MEAN_UPPER, len(cols))
    full_dataset = pd.DataFrame.from_dict(
        {
            col_name: generate_integrated_autocorrelated_series(
                ar_coefficient, mean, STD, x_size + y_size
            )
            for ar_coefficient, mean, col_name in zip(ar_coefficients, means, cols)
        }
    )
    return (
        full_dataset.head(x_size),
        full_dataset.tail(y_size),
        (ar_coefficients, means),
    )
    

class Model:
    def __init__(self, tickers: list[str], x_size: int, y_size: int) -> None:
        self.tickers = tickers
        self.x_size = x_size
        self.y_size = y_size
        self.models: dict[str, ARIMA] = {}

    def train(self, col: str) -> None:
        try:
            with db_con.MetalsPriceDataDatabase() as db:
                conn = db.conn
                for ticker in self.tickers:
                    query = f"SELECT timestamp, rate_price, rate_ask \
                            FROM {ticker}_historic \
                            ORDER BY timestamp DESC LIMIT {self.x_size}"
                    data = pd.read_sql(query, conn)
                    
                    dataset = data[col].values
                    model = ARIMA(order=(1, 1, 0), with_intercept=True, suppress_warnings=True)
                    model.fit(dataset)
                    self.models[ticker] = model
                    
                    ml_logger.info('Creating "{}" price prediction data for "{}"'.format(col, ticker))
        except Exception as e:
            ml_logger.error('An error occured while training the model: {}'.format(e))
            
            
    def save(self, path_to_dir: str | Path) -> None:
        path_to_dir = Path('trained_models', path_to_dir)
        path_to_dir.mkdir(parents=True, exist_ok=True)
        for ticker in self.tickers:
            full_path = path_to_dir / ticker
            self.models[ticker].save(full_path)


def train_price_prediction_models():
    """
    A function to set up multiple training models
    based on multiple data points to use for training.
    """
    try:
        model = Model(COMMODITIES, 12, 1)
        for col in TRAINING_DATA_COLUMNS:
            model.train(col)
            model.save(f"model_{col}")
            
    except Exception as e:
        ml_logger.error('An error occured while training the model: {}'.format(e))