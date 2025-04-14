import pandas as pd
import matplotlib.pyplot as plt

"""
This module contains several data cleaning functions.

Functions
---------
show_na
    Displays all missing values for a particular variable.

plot_na
    Plots missing values.
"""

def show_na(data: pd.DataFrame, variable: str) -> pd.DataFrame:
    """
    Displays all missing values for a given variable.

    This function can be used to quickly access every data point for which
    the value of a particular value is missing.

    Parameters
    ----------
    data : pd.DataFrame
        Original data.

    variable : str
        Variable whose missing values one wishes to detect.

    Returns
    -------
    pd.DataFrame
        Data frame of missing values for a particular variable.
    """

    new_data = data.copy();

    return new_data.loc[new_data[variable].isna()].copy();

def plot_na(data: pd.DataFrame, plotted_variable: str, missing_variable: str, figsize: tuple=(5, 5)) -> None:
    """
    Plots the target variable and shows which timestamps might be missing for a potential predictor.

    This function produces a plot of the target variable and marks the values for which the corresponding values
    of a potential predictor variable are missing with an 'x'.

    Parameters
    ----------
    data : pd.DataFrame
        Data.

    plotted_variable : str
        Target variable.

    missing_variable : str
        Variable whose missing values one wishes to inspect.

    figsize : tuple, default=(5, 5)
        Figure size.
    """

    fig = plt.figure(figsize=figsize);
    ax = fig.subplots(1, 1);

    plot_var = data[plotted_variable];
    missing_var = show_na(data, missing_variable);

    ax.plot(plot_var.index, plot_var, label=plotted_variable, c="b");
    ax.scatter(missing_var.index, missing_var[plotted_variable], label=f"{missing_variable} missing", marker="x", c="r");
    ax.set_title(f"Missing values for {missing_variable}");
    ax.set_xlabel("Timestamps");
    ax.set_ylabel(f"{plotted_variable}");
    ax.legend();
    ax.grid();
    plt.show();

    return;