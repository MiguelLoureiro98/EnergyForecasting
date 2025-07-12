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

    This class implements the naive similar day method first proposed by 
    Conejo et al ([1](#1)). As no training process takes place, only the 
    test data need be provided.

    Parameters
    ----------
    test_data : pd.DataFrame
        Test dataset.

    forecasting_vars : list | str, default="price actual"
        Target forecasting variables.

    Methods
    -------
    forecast(initial_point: str)
        Forecast test set values.

    initial_data_point(data: pd.DataFrame)
        Static method. Used to determine the string that should be passed to the forecast method.

    Notes
    -----
    This method was first proposed by Conejo et al ([1](#1)). Electricity prices for a given day are assumed to be 
    equal to those for a similar day. Similarity is defined by a simple heuristic rule: a Monday is similar to the 
    previous Monday; Tuesdays, Wednesdays, Thursdays, and Fridays are similar to the preceding Monday. 
    This model should only be used as a benchmark to assess the performance of more elaborate forecasting models.

    References
    ----------
    <a id="1">[1]</a> Antonio J. Conejo, Javier Contreras, Rosa Espínola, and Miguel A. Plazas.
    Forecasting electricity prices for a day-ahead pool-based electric energy
    market. International journal of forecasting, 21(3):435–462, 2005.  
    """

    def __init__(self, test_data: pd.DataFrame, forecasting_vars: list | str="price actual") -> None:
        
        self._data = test_data;
        self._vars = forecasting_vars;

        return;

    def forecast(self, initial_point: str) -> pd.DataFrame:
        """
        Forecast test set values.

        This method can used to forecast (future) test set values. The first hour of the first Monday 
        of the test set must be provided as the initial point, as the model can only start predicting 
        values from a Monday. The model will not generate forecasts for data preceding the initial point, 
        although these values will still be used to forecast future values.

        Parameters
        ----------
        initial_point : str
            Date corresponding to the first day whose values should be forecast. The initial_data_point() method 
            can be used to find this data point automatically.

        Returns
        -------
        pd.DataFrame
            Forecasts.
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
        Get the initial data point for forecasting purposes.

        This method can be used to find the initial data point required by the forecast() method.

        Parameters
        ----------
        data : pd.DataFrame
            Test dataset.

        Returns
        -------
        pd.Timestamp
            Timestamp containing the index of the initial data point.
        """

        return (data.loc[data.weekday == 0].index[0] + pd.Timedelta(1, "W"));