import numpy as np
import pandas as pd
import statsmodels.api as sm
import torch
from torch.utils.data import Dataset

"""
This module contains the definitions of all predictive models used for electricity price forecasting.

Classes
-------
NaiveSimilarDay
    Implements the naive similarity-based method.

EPFDataset
    PyTorch implementation of the dataset used for electricity price forecasting.

LSTM
    A simple, customisable LSTM model.
"""

class NaiveSimilarDay():
    """
    Implements the naive similarity-based method.

    This class implements the naive similar day method first proposed by 
    Conejo et al ([1](#1)). As no training process takes place, only the 
    test data need be provided.

    Parameters
    ----------
    test_data : pd.DataFrame
        Test dataset.

    forecasting_vars : list | str, default="price actual"
        Target forecasting variables.

    Methods
    -------
    forecast(initial_point: str)
        Forecast test set values.

    initial_data_point(data: pd.DataFrame)
        Static method. Used to determine the string that should be passed to the forecast method.

    Notes
    -----
    This method was first proposed by Conejo et al ([1](#1)). Electricity prices for a given day are assumed to be 
    equal to those for a similar day. Similarity is defined by a simple heuristic rule: a Monday is similar to the 
    previous Monday; Tuesdays, Wednesdays, Thursdays, and Fridays are similar to the preceding Monday. 
    This model should only be used as a benchmark to assess the performance of more elaborate forecasting models.

    References
    ----------
    <a id="1">[1]</a> Antonio J. Conejo, Javier Contreras, Rosa Espínola, and Miguel A. Plazas.
    Forecasting electricity prices for a day-ahead pool-based electric energy
    market. International journal of forecasting, 21(3):435–462, 2005.  
    """

    def __init__(self, test_data: pd.DataFrame, forecasting_vars: list | str="price actual") -> None:
        
        self._data = test_data;
        self._vars = forecasting_vars;

        return;

    def forecast(self, initial_point: str) -> pd.DataFrame:
        """
        Forecast test set values.

        This method can used to forecast (future) test set values. The first hour of the first Monday 
        of the test set must be provided as the initial point, as the model can only start predicting 
        values from a Monday. The model will not generate forecasts for data preceding the initial point, 
        although these values will still be used to forecast future values.

        Parameters
        ----------
        initial_point : str
            Date corresponding to the first day whose values should be forecast. The initial_data_point() method 
            can be used to find this data point automatically.

        Returns
        -------
        pd.DataFrame
            Forecasts.
        """

        data = self._data.copy();

        forecasts = data.shift(24*7);
        forecasts = forecasts.loc[initial_point:].copy();
        tuesdays = data.shift(24);
        wednesdays = data.shift(48);
        thursdays = data.shift(72);
        fridays = data.shift(96);

        forecasts.loc[forecasts.weekday == 1] = tuesdays.loc[tuesdays.weekday == 0].loc[initial_point:].replace({"weekday": 0}, 1);
        forecasts.loc[forecasts.weekday == 2] = wednesdays.loc[wednesdays.weekday == 0].loc[initial_point:].replace({"weekday": 0}, 2);
        forecasts.loc[forecasts.weekday == 3] = thursdays.loc[thursdays.weekday == 0].loc[initial_point:].replace({"weekday": 0}, 3);
        forecasts.loc[forecasts.weekday == 4] = fridays.loc[fridays.weekday == 0].loc[initial_point:].replace({"weekday": 0}, 4);

        return forecasts[self._vars].copy();

    @staticmethod
    def initial_data_point(data: pd.DataFrame) -> pd.Timestamp:
        """
        Get the initial data point for forecasting purposes.

        This method can be used to find the initial data point required by the forecast() method.

        Parameters
        ----------
        data : pd.DataFrame
            Test dataset.

        Returns
        -------
        pd.Timestamp
            Timestamp containing the index of the initial data point.
        """

        return (data.loc[data.weekday == 0].index[0] + pd.Timedelta(1, "W"));

class EPFDataset(Dataset):
    """
    PyTorch implementation of the dataset used for electricity price forecasting.

    This class implements the electricity price forecasting dataset using PyTorch. \
    The number of past lags that will be used to forecast the target variables \
    can be changed via the n_lags property.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe containing the dataset.

    targets : list[str] | str, default="price actual"
        Target or list of targets. The default is "price actual".

    forecasting_vars : list[str] | str, default="price actual"
        Forecasting variable(s). These are the variables used to \
        forecast the targets. The default is "price actual".

    lags : int, default=24
        Number of past lags to consider. The default is 24 (= 1 day).

    Attributes
    ----------
    n_lags
        Number of past lags to consider.
    """

    def __init__(self, data: pd.DataFrame, 
                 targets: list[str] | str="price actual", 
                 forecasting_vars: list[str] | str="price actual",
                 lags: int=24) -> None:

        super().__init__();
        self._data = data;

        if(type(targets) == str):

            targets = [targets];
        
        if(type(forecasting_vars) == str):

            forecasting_vars = [forecasting_vars];

        self._target_cols = targets;
        self._features = forecasting_vars;
        self._n = lags;
    
        return;

    @property
    def n_lags(self) -> int:

        return self._n;

    @n_lags.setter
    def n_lags(self, lags) -> None:

        self._n = lags;

        return;

    def __len__(self) -> int:

        return self._data.shape[0] - self._n;

    def __getitem__(self, index) -> tuple[torch.Tensor, torch.Tensor]:

        X = torch.tensor(self._data[self._features].iloc[index : index + self._n].to_numpy());
        y = torch.tensor(self._data[self._target_cols].iloc[index + self._n].to_numpy());

        #if(len(self._features) == 1):

        #    X = torch.unsqueeze(X, 1);
        
        #if(len(self._target_cols) == 1):

        #    y = torch.unsqueeze(y, 1);

        return X, y;

class LSTM(torch.nn.Module):
    """
    Simple, customisable LSTM model.

    This class implements a simple LSTM model. Parameters such as the LSTM layers,
    the number of features the model should consider, or the size of the hidden
    state should be defined by the user.

    Parameters
    ----------
    n_layers : int, default=1
        Number of LSTM layers.

    n_features : int, default=1
        Number of features.

    hidden_size : int, default=32
        LSTM hidden state size.

    Methods
    -------
    forward(X: torch.Tensor)
        Perform the forward pass.
    """

    def __init__(self, n_layers: int=1, n_features: int=1, hidden_size: int=32) -> None:

        super().__init__();
        self.lstm_layer = torch.nn.LSTM(n_features, hidden_size, n_layers, batch_first=True);
        self.linear_layer = torch.nn.Linear(hidden_size, 1);

        return;

    def forward(self, X: torch.Tensor) -> torch.Tensor:
        """
        Performs the forward pass.

        This method performs the model's forward pass.

        Parameters
        ----------
        X : torch.Tensor
            Input tensor. Should be of shape (batch, n_obs, n_features).

        Returns
        -------
        torch.Tensor
            Output tensor containing the model's forecasts.
        """

        x, _ = self.lstm_layer(X);
        x = x[:, -1, :];
        y = self.linear_layer(x);

        return y;

def _train_one_epoch(model: LSTM, 
                     loader: torch.utils.data.DataLoader, 
                     loss_fcn: torch.nn.MSELoss, 
                     optimiser: torch.optim.Adam,
                     device: torch.device) -> float:
    
    """Runs a single training epoch."""

    running_loss = 0;

    for X, y in loader:

        X, y = X.to(device), y.to(device);

        optimiser.zero_grad();
        preds = model(X);
    
        loss = loss_fcn(preds, y);
        loss.backward();
        optimiser.step();
    
        running_loss += loss;

    return running_loss;

def _validation(model: LSTM,
                loader: torch.utils.data.DataLoader, 
                loss_fcn: torch.nn.MSELoss, 
                device: torch.device) -> float:

    """Computes the validation loss for a single epoch."""

    val_loss = 0;

    with torch.no_grad():

        for X, y in loader:

            X, y = X.to(device), y.to(device);

            preds = model(X);
            val_loss += loss_fcn(preds, y);

    return val_loss;

def model_training(model: LSTM, 
                   device: torch.device, 
                   training_loader: torch.utils.data.DataLoader,
                   validation_loader: torch.utils.data.DataLoader,
                   loss_fcn: torch.nn.MSELoss,
                   optimiser: torch.optim.Adam,
                   epochs: int=200) -> tuple[np.ndarray]:
    """
    Executes the model training procedure.

    Parameters
    ----------
    model : LSTM
        An instance of the LSTM model class. 
        Should be moved to the correct device before calling this function.

    device : torch.device
        Device where training should be performed.

    training_loader : torch.utils.data.DataLoader
        Training set DataLoader.

    validation_loader : torch.utils.data.DataLoader
        Validation set DataLoader.

    loss_fcn : torch.nn.MSELoss
        Loss function.

    optimiser : torch.optim.Adam
        Optimiser.

    epochs : int, default=200
        Number of epochs.

    Returns
    -------
    tuple[np.ndarray]
        Tuple containing the arrays of training and validation losses.
    """
    
    #model.to(device);

    training_loss = torch.zeros((epochs, 1), dtype=torch.float64, device=device);
    validation_loss = torch.zeros((epochs, 1), dtype=torch.float64, device=device);

    for epoch in range(epochs):

        model.train();

        training_loss[epoch] = _train_one_epoch(model, training_loader, loss_fcn, optimiser, device) / len(training_loader.dataset);
    
        model.eval();

        validation_loss[epoch] = _validation(model, validation_loader, loss_fcn, device) / len(validation_loader.dataset);
    
        print(f"Finished epoch {epoch+1} of {epochs}.");

    return training_loss, validation_loss;