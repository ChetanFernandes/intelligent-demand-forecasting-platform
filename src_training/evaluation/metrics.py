import numpy as np
from sklearn.metrics import mean_absolute_error, root_mean_squared_error

def _prepare_inputs(y_true, y_pred):

    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()

    if len(y_true) != len(y_pred):
        raise ValueError(
            f"Shape mismatch: y_true={y_true.shape}, y_pred={y_pred.shape}"
        )

    return y_true, y_pred

def calculate_mae(y_true,y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    return mae

def calculate_rmse(y_true,y_pred):
    rmse = root_mean_squared_error(y_true, y_pred)
    return rmse

def calculate_mape(y_true,y_pred):
    """
    Calculate Mean Absolute Percentage Error (MAPE).
    Ignores observations where the actual value is zero to avoid division-by-zero errors.

    Parameters
    ----------
    y_true : array-like Actual target values.

    y_pred : array-like. Predicted target values.

    Returns
    -------
    float
        MAPE expressed as a percentage.
    """

    y_true, y_pred = _prepare_inputs(y_true, y_pred)

    mask = y_true != 0

    if not np.any(mask):
        return np.nan
    
    mape = np.mean(np.abs((y_true[mask]-y_pred[mask])/y_true[mask]))

    return float(mape * 100)

def calculate_smape(y_true, y_pred):
    """
    Calculate Symmetric Mean Absolute Percentage Error (SMAPE).

    Parameters
    ----------
    y_true : array-like
        Actual target values.

    y_pred : array-like
        Predicted target values.

    Returns
    -------
    float
        SMAPE expressed as a percentage.
    """

    y_true, y_pred = _prepare_inputs(y_true, y_pred)

    denominator = np.abs(y_true) + np.abs(y_pred)

    mask = denominator != 0

    if not np.any(mask):
        return np.nan

    smape = np.mean(2 * np.abs(y_true[mask] - y_pred[mask]) / denominator[mask])

    return float(smape * 100)

def calculate_wape(y_true, y_pred):
    """
    Calculate Weighted Absolute Percentage Error (WAPE).

    Parameters
    ----------
    y_true : array-like
        Actual target values.

    y_pred : array-like
        Predicted target values.

    Returns
    -------
    float
        WAPE expressed as a percentage.
    """

    y_true, y_pred = _prepare_inputs(y_true, y_pred)

    
    numerator = np.sum(np.abs(y_true - y_pred))

    denominator = np.sum(np.abs(y_true))

    if denominator == 0:
        return np.nan

    wape = numerator / denominator

    return float(wape * 100)


def calculate_rmsse(y_train,y_true,y_pred):
    """
    Calculate Root Mean Squared Scaled Error (RMSSE).

    Parameters
    ----------
    y_train : array-like
        Historical training values.

    y_true : array-like
        Actual values.

    y_pred : array-like
        Predicted values.

    Returns
    -------
    float
        RMSSE score.

    """
    y_train = np.asarray(y_train).ravel()
    y_true = np.asarray(y_true).ravel()
    y_pred = np.asarray(y_pred).ravel()

    # Mean squared error
    mse = np.mean((y_true - y_pred)**2)

    # Naive forecast denominator
    naive_mse = np.mean(np.diff(y_train) ** 2)

    if naive_mse == 0:
        return np.nan

    rmsse = np.sqrt(mse / naive_mse)

    return float(rmsse)



