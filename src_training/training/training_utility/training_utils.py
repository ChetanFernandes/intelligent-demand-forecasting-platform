import time
from src_training.evaluation.metrics_calculator import MetricsCalculator
from src_training.evaluation.metrics import calculate_rmsse


def train_and_evaluate(trainer, X_train_sample, y_train_sample, X_val, Y_val, model_params):

    start = time.time()

    model = trainer.train(X_train_sample, y_train_sample, X_val, Y_val, **model_params)

    training_time = time.time() - start

    print(f"Training Time: {training_time:.2f} seconds")

    print("Model trained successfully")

    predictions = model.predict(X_val)

    metrics = MetricsCalculator.calculate_metrics(y_true = Y_val, y_pred = predictions)

    rmsse = calculate_rmsse(y_train = y_train_sample, y_true = Y_val, y_pred = predictions)

    
    print(f"mae: {metrics["mae"]}")
    print(f"rmse: {metrics["rmse"]}")
    print(f"mape: {metrics["mape"]}")
    print(f"smape: {metrics["smape"]}")
    print(f"wape: {metrics["wape"]}")
    print(f"rmsse: {rmsse}")



    return (
    model,
    metrics["mae"],
    metrics["rmse"],
    metrics["mape"],
    metrics["smape"],
    metrics["wape"],
    rmsse,
    training_time,
)
