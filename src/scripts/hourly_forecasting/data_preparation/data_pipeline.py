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
    Executes the data preprocessing pipeline for forecasting tasks.

    This function executes the entire data preprocessing procedure for forecasting tasks.
    This includes date/time conversion, the creation of a time zone offset indicator variable,
    and data frame concatenation operations. Data cleaning, normalisation, and smoothing
    operations are not included, and will have to be performed using separate functions.

    Parameters
    ----------
    energy_data : pd.DataFrame
        Energy generation data frame.

    weather_data : pd.DataFrame
        Weather features data frame.

    Returns
    -------
    pd.DataFrame
        Data frame formatted for forecasting tasks.
    """

    # Deep copies
    new_energy_data = energy_data.copy();
    new_weather_data = weather_data.copy();

    new_energy_data = create_tz_column(new_energy_data, "time");
    new_energy_data = datetime_conversion(new_energy_data, "time");
    new_weather_data = create_tz_column(new_weather_data, "dt_iso");
    new_weather_data = datetime_conversion(new_weather_data, "dt_iso");

    # Remove duplicate rows
    new_weather_list = [new_weather_data.groupby("city_name").get_group(city) for city in new_weather_data["city_name"].unique()];
    weather_list_no_dups = [df.loc[(~df.index.duplicated()).tolist()] for df in new_weather_list];
    
    # Rename columns
    old_names_list = [df.columns[1:].tolist() for df in weather_list_no_dups];
    city_names = [df["city_name"].unique().item() for df in weather_list_no_dups];
    new_names_list = [[name + city_name for name in cols] for cols, city_name in zip(old_names_list, city_names)];
    name_dicts = [{old_name: new_name for old_name, new_name in zip(old_cols, new_cols)} for old_cols, new_cols in zip(old_names_list, new_names_list)];
    weather_list_no_dups_new_cols = [df.drop(columns="city_name").rename(columns=name_dict) for df, name_dict in zip(weather_list_no_dups, name_dicts)];
    
    # Concatenate weather data frames
    processed_weather_data = pd.concat(weather_list_no_dups_new_cols, axis=1);

    # Concatenate energy and weather data frames
    new_data = pd.concat([new_energy_data, processed_weather_data], axis=1);

    return new_data;