import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
This module contains data visualisation functions.
"""

def moving_average_plot(data: pd.DataFrame, vars: list[str], lags: int) -> None:
    """
    Plot moving averages together with the original values.

    _extended_summary_

    Parameters
    ----------
    data : pd.DataFrame
        Dataset of interest.

    vars : list[str]
        List of relevants whose moving average should be computed and plotted.

    lags : int
        Number of lags to consider for moving average calculations.
    """

    renamed_vars = [f"ma_{var}" for var in vars];
    renaming_dict = {name: rename for (name, rename) in zip(vars, renamed_vars)};

    ma = data[vars].rolling(lags).mean().rename(columns=renaming_dict);
    concat_data = pd.concat([data[vars].copy(), ma], axis=1);
    concat_data.plot(kind="line", title=f"Moving average plots for {vars} - {lags} lags", xlabel="Date");

    return;

def smoothing_plot(data: pd.DataFrame, vars: list[str], lags: int, alpha: float) -> None:

    pass

def diff_lag_plot(data: pd.DataFrame, var: str, lag: int) -> None:

    pass

def cross_lag_plot(data: pd.DataFrame, var_x: str, var_y: str, lag_x: int, lag_y: int) -> None:

    pass

def cross_diff_lag_plot(data: pd.DataFrame, var_x: str, var_y: str, lag_x: int, lag_y: int) -> None:

    pass

#def recurrence_plot(data: pd.DataFrame, vars: list[str]) -> None:

#    pass