
def log_experiment(tracker, model, mae, rmse, mape, smape, wape, rmsse , training_time, importance_df, feature_importance_path, X_train_sample
                   ,alogorthm_name_tag):

    tracker.log_params(model.get_params())

    tracker.log_params({"sample_size": len(X_train_sample)})

    tracker.log_metrics({"mae": mae, "rmse": rmse, "mape":mape, "smape":smape, "wape":wape, "rmsse":rmsse, "training_time": training_time})

    tracker.log_tags({
        "dataset": "M5 Forecasting",
        "model_type": alogorthm_name_tag
    })



    tracker.log_model(model)

    importance_df.to_csv(feature_importance_path, index=False)

    tracker.log_artifact(feature_importance_path)


def log_experiment_hyper(tracker, best_params, best_rmse, stratergy):

    tracker.log_params(best_params)

    tracker.log_metrics({"rmse": best_rmse,})

    tracker.log_tags({
        "dataset": "M5 Forecasting",
        "staratergy": stratergy
    })

 

