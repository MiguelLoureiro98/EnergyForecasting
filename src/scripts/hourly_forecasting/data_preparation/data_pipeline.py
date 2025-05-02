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
    
    # Concatenate data frames
    old_names_list = [df.columns.tolist() for df in weather_list_no_dups];
    city_names = [df["city_name"].unique().item() for df in weather_list_no_dups];
    new_names_list = [[name + city_name for name in cols] for cols, city_name in zip(old_names_list, city_names)];
    name_dicts = [[{old_name: new_name} for old_name, new_name in zip(old_cols, new_cols)] for old_cols, new_cols in zip(old_names_list, new_names_list)];
    weather_list_no_dups_new_cols = [df.rename(name_dict) for df, name_dict in zip(weather_list_no_dups, name_dicts)];
    new_data = pd.concat(weather_list_no_dups_new_cols, axis=1);

    return new_data;