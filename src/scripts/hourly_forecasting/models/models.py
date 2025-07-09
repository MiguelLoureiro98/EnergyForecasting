import numpy as np
import pandas as pd
import statsmodels.api as sm
import torch

"""
This module contains the definitions of all predictive models used for electricity price forecasting.

Classes
-------
NaiveSimilarDay
    Implements the naive similarity-based method.
"""

class NaiveSimilarDay():

    def __init__(self, prev_week: pd.DataFrame) -> None:
        
        self._weekday = prev_week.loc[prev_week["weekday"] == 0].copy();
        self._saturday = prev_week.loc[prev_week["weekday"] == 5].copy();
        self._sunday = prev_week.loc[prev_week["weekday"] == 5].copy();

        return;

    def forecast(self, data: pd.DataFrame, horizon: int=1) -> np.ndarray | pd.DataFrame:

        current_time = data.tail(1).index[0] + pd.Timedelta(1, unit="h");
        forecasting_timestamps = pd.date_range(start=current_time, periods=horizon, freq="h");

        forecast_idx = forecasting_timestamps.to_series();
        weekday = forecast_idx.dt.weekday;
        hour = forecast_idx.dt.hour;
        forecasts = pd.concat([forecast_idx, weekday, hour], axis=1).rename(columns={0: "timestamp", 1: "weekday", 2: "hour"});

        

        return forecasts;

    @staticmethod
    def prev_week_data(data: pd.DataFrame) -> pd.DataFrame:

        pass