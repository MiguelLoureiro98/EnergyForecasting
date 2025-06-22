import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

"""
This module includes functions that facilitate statistical time series analysis.

Functions
---------
stationarity_tests
    Performs two distinct stationarity tests.
"""

def stationarity_tests(time_series: pd.Series) -> tuple:
    """
    Performs two distinct stationarity tests.

    This function can be used to assess the stationarity of a given
    time series by performing the Augmented Dickey-Fuller test and
    the KPSS test.

    Parameters
    ----------
    time_series : pd.Series
        Time series of interest.

    Returns
    -------
    tuple
        Test results.
    """

    adf_test = sm.tsa.adfuller(time_series, autolag="BIC");
    adf_indices = ["ADF test statistic", "p-value", "#Lags", "#Observations"];
    adf_indices.extend(["Critical value ({})".format(level) for level in adf_test[4].keys()]);
    adf_values = list(adf_test[:4]);
    adf_values.extend([val for val in adf_test[4].values()]);
    adf_results = pd.Series(adf_values, index=adf_indices);

    kpss_test = sm.tsa.kpss(time_series);
    kpss_indices = ["KPSS test statistic", "p-value", "#Lags"];
    kpss_indices.extend(["Critical value ({})".format(level) for level in kpss_test[3].keys()]);
    kpss_values = list(kpss_test[:3]);
    kpss_values.extend([val for val in kpss_test[3].values()]);
    kpss_results = pd.Series(kpss_values, index=kpss_indices);

    print("ADF test results");
    print("-" * 16);
    print(adf_results);

    print("\nKPSS test results");
    print("-" * 17);
    print(kpss_results);
    
    return;