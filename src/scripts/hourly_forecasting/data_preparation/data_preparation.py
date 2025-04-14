import pandas as pd

"""
This module contains date/time conversion and generic data preparation functions.

Functions
---------
create_tz_column
    Creates a time zone indicator variable.

datetime_conversion
    Converts the data frame's index to a datetime object.
"""

def create_tz_column(data: pd.DataFrame, time_column: str) -> pd.DataFrame:
    """
    Creates a time zone indicator column and adds it to the data frame.

    Parameters
    ----------
    data : pd.DataFrame
        Original data.

    time_column : str
        Name of the column containing the timestamps.

    Returns
    -------
    pd.DataFrame
        New data frame containing the time zone indicator column.
    """

    new_data = data.copy();

    new_data.loc[new_data[time_column].str.contains("+01:00", regex=False), "tz_offset"] = 1;
    new_data.loc[new_data[time_column].str.contains("+02:00", regex=False), "tz_offset"] = 2;

    return new_data;

def datetime_conversion(data: pd.DataFrame, time_column: str) -> pd.DataFrame:
    """
    Converts the index to a date/time object.

    Parameters
    ----------
    data : pd.DataFrame
        Original data.

    time_column : str
        Name of the column containing the timestamps.

    Returns
    -------
    pd.DataFrame
        Data frame with a date/time index.
    """

    new_data = data.copy();

    new_data[time_column] = pd.to_datetime(new_data[time_column], utc=True);
    new_data = new_data.set_index(time_column);

    return new_data;