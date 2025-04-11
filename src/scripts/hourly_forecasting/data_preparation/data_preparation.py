import pandas as pd

"""
This file contains date/time conversion and generic data preparation functions.
"""

def create_tz_column(data: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a time zone indicator column and add it to the data frame.

    Parameters
    ----------
    data : pd.DataFrame
        Original data.

    Returns
    -------
    pd.DataFrame
        New data frame containing the time zone indicator column.
    """

    new_data = data.copy();

    new_data.loc[new_data.time.str.contains("+01:00", regex=False), "tz_offset"] = 1;
    new_data.loc[new_data.time.str.contains("+02:00", regex=False), "tz_offset"] = 2;

    return new_data;

def datetime_conversion(data: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the index to a date/time object.

    Parameters
    ----------
    data : pd.DataFrame
        Original data.

    Returns
    -------
    pd.DataFrame
        Data frame with a date/time index.
    """

    new_data = data.copy();

    new_data["time"] = pd.to_datetime(new_data["time"], utc=True);

    return new_data;