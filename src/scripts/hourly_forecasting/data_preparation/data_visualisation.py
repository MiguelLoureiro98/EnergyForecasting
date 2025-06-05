import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
This module contains data visualisation functions.

Functions
---------
moving_average_plot
    Plots moving averages together with the original values.

diff_lag_plot
    Creates a lag plot of a differenced time series.

cross_lag_plot
    Creates a lag plot of two different variables.
"""

def moving_average_plot(data: pd.DataFrame, vars: list[str], lags: int) -> None:
    """
    Plots moving averages together with the original values.

    This function can be used to create a plot containing the original values of multiple
    time series and their moving averages.

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

def diff_lag_plot(data: pd.DataFrame, var: str, lag: int) -> None:
    """
    Creates a lag plot of a differenced time series.

    This function can be used to create a lag plot of a differenced time
    series with a custom number of lags.

    Parameters
    ----------
    data : pd.DataFrame
        Dataset of interest.

    var : str
        Variable of interest.

    lag : int
        Number of lags to consider for lag plot.
    """

    data_var = data[var].diff().copy();
    pd.plotting.lag_plot(data_var, lag);

    return;

def cross_lag_plot(data: pd.DataFrame, var_x: str, var_y: str, lag_x: int, lag_y: int) -> None:
    """
    Creates a lag plot of two different variables.

    This function can be used to create a lag plot where the x variable is different from the
    y variable. The influence of past values of an external time series on a target series
    can thus be assessed.

    Parameters
    ----------
    data : pd.DataFrame
        Dataset of interest.

    var_x : str
        Independent variable.

    var_y : str
        Dependent variable.

    lag_x : int
        Lags to consider for the dependent variable.

    lag_y : int
        Lags to consider for the independent variable.
    """

    data_x = data[var_x].shift(lag_x).copy();
    data_y = data[var_y].shift(lag_y).copy();

    pd.concat([data_x, data_y], axis=1).\
    plot(kind="scatter", x=f"{var_x}", y=f"{var_y}", title=f"Cross lag plot: {var_x} and {var_y}", xlabel=f"{var_x} (t + {lag_x})", ylabel=f"{var_y} (t + {lag_y})");

    return;

def cross_diff_lag_plot(data: pd.DataFrame, var_x: str, var_y: str, lag_x: int, lag_y: int) -> None:
    """
    Creates a lag plot of two differenced time series.

    This function can be used to create a lag plot where the x variable is different from the
    y variable. Both time series are differenced before the plot is created. The influence of 
    past variations of an external time series on those of a target series can thus be assessed.

    Parameters
    ----------
    data : pd.DataFrame
        Dataset of interest.

    var_x : str
        Independent variable.

    var_y : str
        Dependent variable.

    lag_x : int
        Lags to consider for the dependent variable.

    lag_y : int
        Lags to consider for the independent variable.
    """

    data_x = data[var_x].diff().shift(lag_x).copy();
    data_y = data[var_y].diff().shift(lag_y).copy();

    pd.concat([data_x, data_y], axis=1).\
    plot(kind="scatter", x=f"{var_x}", y=f"{var_y}", title=f"Cross differenced lag plot: $\Delta$ {var_x} and $\Delta$ {var_y}", xlabel=f" $\Delta$ {var_x} (t + {lag_x})", ylabel=f"$\Delta$ {var_y} (t + {lag_y})");

    return;

def monthly_averages(data: pd.DataFrame, var: str) -> None:
    """
    Plots monthly averages.

    This function can be used to create monthly average plots for a single variable.

    Parameters
    ----------
    data : pd.DataFrame
        Dataset of interest.

    var : str
        Variable of interest.
    """

    new_data = data.loc[var].copy();
    new_data = pd.concat([new_data, new_data.index.to_series().dt.month], axis=1).\
               rename(columns={0: "month"}).\
               groupby("month").mean().\
               plot(kind="bar", title=f"Average monthly {var}", xlabel="Months", ylabel=f"{var}");

    return;

def weekday_averages(data: pd.DataFrame, var: str) -> None:
    """
    Plots average values by weekday.

    This function can be used to create weekday average plots for a single variable.

    Parameters
    ----------
    data : pd.DataFrame
        Dataset of interest.

    var : str
        Variable of interest.
    """

    errors = data.groupby("weekday")[var].std();
    data.groupby("weekday")[var].mean().plot(kind="bar", yerr=errors, title=f"{var} weekday average", xlabel="Weekday", ylabel=f"{var}");

    return;

def hourly_averages(data: pd.DataFrame, var: str) -> None:
    """
    Plots hourly average values.

    This function can be used to create hourly average plots for a single variable.

    Parameters
    ----------
    data : pd.DataFrame
        Dataset of interest.

    var : str
        Variable of interest.
    """

    errors = data.groupby("hour")[var].std();
    data.groupby("hour")[var].mean().plot(kind="bar", yerr=errors, title=f"Average hourly {var}", xlabel="Hours", ylabel=f"{var}");

    return;