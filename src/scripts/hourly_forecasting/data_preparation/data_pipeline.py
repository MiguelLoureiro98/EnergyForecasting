import pandas as pd
from scripts.hourly_forecasting.data_preparation.data_preparation import create_tz_column, datetime_conversion
from scripts.hourly_forecasting.data_preparation.data_cleaning import show_na, plot_na

"""
This module contains the preprocessing pipeline for forecasting tasks.

Functions
---------
prepare_data_forecasting
    Executes the full data preprocessing pipeline for forecasting tasks.
"""

def prepare_data_forecasting(energy_data: pd.DataFrame, weather_data: pd.DataFrame) -> pd.DataFrame:
    """
    _summary_

    _extended_summary_

    Parameters
    ----------
    energy_data : pd.DataFrame
        _description_

    weather_data : pd.DataFrame
        _description_

    Returns
    -------
    pd.DataFrame
        _description_
    """

    # Deep copy
    new_energy_data = energy_data.copy();
    new_weather_data = weather_data.copy();

    new_energy_data = create_tz_column(new_energy_data, "time");
    new_energy_data = datetime_conversion(new_energy_data, "time");
    new_weather_data = create_tz_column(new_weather_data, "dt_iso");
    new_weather_data = datetime_conversion(new_weather_data, "dt_iso");

    # Remove duplicate rows
    new_weather_list = [new_weather_data.groupby("city_name").get_group(city) for city in new_weather_data["city_name"].unique()];
    weather_list_no_dups = [df.loc[(~df.index.duplicated()).tolist()] for df in new_weather_list];
    
    

    new_data = 0;

    return new_data;