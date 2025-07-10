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
    """
    Implements the naive similarity-based method.

    This class implements Nogales' naive similarity-based method for electricity price forecasting.
    ...

    Parameters
    ----------
    test_data : pd.DataFrame
        ...

    forecasting_vars : list | str, default="price actual"
        ...

    Methods
    -------
    forecast(initial_point: str)
        ...

    initial_data_point(data: pd.DataFrame)
        ...
    """

    def __init__(self, test_data: pd.DataFrame, forecasting_vars: list | str="price actual") -> None:
        
        self._data = test_data;
        self._vars = forecasting_vars;

        return;

    def forecast(self, initial_point: str) -> pd.DataFrame:
        """
        _summary_

        _extended_summary_

        Parameters
        ----------
        initial_point : str
            _description_

        Returns
        -------
        pd.DataFrame
            _description_
        """

        data = self._data.copy();

        forecasts = data.shift(24*7);
        forecasts = forecasts.loc[initial_point:].copy();
        tuesdays = data.shift(24);
        wednesdays = data.shift(48);
        thursdays = data.shift(72);
        fridays = data.shift(96);

        forecasts.loc[forecasts.weekday == 1] = tuesdays.loc[tuesdays.weekday == 0].loc[initial_point:].replace({"weekday": 0}, 1);
        forecasts.loc[forecasts.weekday == 2] = wednesdays.loc[wednesdays.weekday == 0].loc[initial_point:].replace({"weekday": 0}, 2);
        forecasts.loc[forecasts.weekday == 3] = thursdays.loc[thursdays.weekday == 0].loc[initial_point:].replace({"weekday": 0}, 3);
        forecasts.loc[forecasts.weekday == 4] = fridays.loc[fridays.weekday == 0].loc[initial_point:].replace({"weekday": 0}, 4);

        return forecasts[self._vars].copy();

    @staticmethod
    def initial_data_point(data: pd.DataFrame) -> pd.Timestamp:
        """
        _summary_

        _extended_summary_

        Parameters
        ----------
        data : pd.DataFrame
            _description_

        Returns
        -------
        pd.Timestamp
            _description_
        """

        return (data.loc[data.weekday == 0].index[0] + pd.Timedelta(1, "W"));