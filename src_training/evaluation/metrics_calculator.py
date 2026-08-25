from src_training.evaluation.metrics import calculate_mae, calculate_rmse, calculate_mape,calculate_smape,calculate_wape

class MetricsCalculator:
    """
    Computes all evaluation metrics for model predictions.
    """

    @staticmethod
    def calculate_metrics(y_true,y_pred):
        return {
                "mae":   calculate_mae(y_true,y_pred),
                "rmse": calculate_rmse(y_true,y_pred),
                "mape" :  calculate_mape(y_true,y_pred),
                "smape" : calculate_smape(y_true,y_pred),
                "wape": calculate_wape(y_true, y_pred),
                }
    
    
    
    