import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""
This module contains feature-engineering-related functions.

Functions
---------
construct_features
    Constructs features from one or more raw features.
"""

def construct_features(data: pd.DataFrame) -> pd.DataFrame:
    """
    Constructs features from one or more raw features.

    This function constructs that might be useful for electricity price forecasting,
    such as total generation, reserve margin, etc. from raw features. It returns a 
    new data frame containing both raw and engineered features.

    Parameters
    ----------
    data : pd.DataFrame
        Dataset containing only raw features.

    Returns
    -------
    pd.DataFrame
        Dataset containing engineered features.
    """

    # Read capacity data
    data_path = "../../../data/Europe_Installed_Capacity_Power_Generation/Spain/InstalledCapacity_Spain.csv";
    capacity_data = pd.read_csv(data_path);

    # Column name construction
    stable_renewables = ["Hydro Water Reservoir", "Hydro Pumped Storage"];
    renewables = stable_renewables.extend(["Biomass", "Hydro Run-of-river and poundage", "Waste", "Solar", "Wind Onshore"]);
    stable_renewables_original = ["generation " + ren.lower() for ren in stable_renewables];
    renewables_original = ["generation " + ren.lower() for ren in renewables];

    gen_cols_original = data.columns[data.columns.str.contains("generation")];

    # Feature construction
    weekday = data.index.to_series().dt.dayofweek;
    hour = (data.index.to_series().dt.hour + data["tz_offset"]).astype("int32");
    new_data = pd.concat([data, weekday, hour]).rename(columns={0: "weekday", 1: "hour"});

    total_capacity = capacity_data[["2015 (MW)", "2016 (MW)", "2017 (MW)", "2018 (MW)"]].sum(axis=0);
    stable_renewable_capacity = capacity_data.loc[capacity_data["Production Type"].isin(stable_renewables), ["2015 (MW)", "2016 (MW)", "2017 (MW)", "2018 (MW)"]].copy();
    renewable_capacity = capacity_data.loc[capacity_data["Production Type"].isin(renewables), ["2015 (MW)", "2016 (MW)", "2017 (MW)", "2018 (MW)"]].copy();

    total_gen = data[gen_cols_original].sum(axis=1);
    stable_renewable_gen = data[stable_renewables_original].sum(axis=1);
    renewable_gen = data[renewables_original].sum(axis=1);
    new_data = pd.concat([new_data, total_gen, stable_renewable_gen, renewable_gen]).rename(columns={0: "total_gen", 1: "stable_renweable_gen", 2: "renewable_gen"});

    return new_data;