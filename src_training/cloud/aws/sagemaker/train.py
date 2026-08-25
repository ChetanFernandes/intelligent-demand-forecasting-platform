import argparse
import os
import pandas as pd
#from lightgbm import LGBMRegressor, early_stopping
#from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from sklearn.metrics import root_mean_squared_error
import joblib

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float)
    parser.add_argument("--depth", type=int)
    parser.add_argument("--l2_leaf_reg", type=float)
    parser.add_argument("--random_strength", type=float)
    parser.add_argument("--border_count", type=float)
    parser.add_argument("--subsample", type=float)
    parser.add_argument("--rsm", type=float)
    parser.add_argument("--min_data_in_leaf", type=int)
    parser.add_argument("--iterations", type=int)
    '''
    Suppose SageMaker runs your script like this:

   python train.py \
    --learning-rate 0.05 \
    --num-leaves 64 \
    --max-depth 10 \
    --min-child-samples 20 \
    --n-estimators 300
    '''

    args = parser.parse_args() 
    # parse_args() converts that into a Python object
    '''
    args
│
        ├── learning_rate = 0.05
        ├── num_leaves = 64
        ├── max_depth = 10
        ├── min_child_samples = 20
        └── n_estimators = 300
    '''

    train_data_dir = os.environ["SM_CHANNEL_TRAIN"] # This is the directory where sagemake stores the training data in EC2 istance
    # it conatins /opt/ml/input/data/train

    model_dir = os.environ["SM_MODEL_DIR"]
    # /opt/ml/model/model.joblib

    X_train = pd.read_parquet(os.path.join(train_data_dir, "X_train.parquet"))

    print("X_train shape:", X_train.shape)
    print("\nX_train dtypes:")
    print(X_train.dtypes)

    y_train = pd.read_parquet(os.path.join(train_data_dir, "Y_train.parquet")).squeeze() 

    # squeeze converts df to series

    # Use squeeze() only when you're expecting a single column and you want it as a Series instead of a DataFrame.

    X_val = pd.read_parquet(os.path.join(train_data_dir, "X_val.parquet"))
    
    y_val = pd.read_parquet(os.path.join(train_data_dir, "Y_val.parquet")).squeeze() 

    ''' 
    model = LGBMRegressor(
        learning_rate=args.learning_rate,
        num_leaves=args.num_leaves,
        max_depth=args.max_depth,
        min_child_samples=args.min_child_samples,
        colsample_bytree=args.colsample_bytree,
        subsample=args.subsample,
        subsample_freq=args.subsample_freq,
        min_split_gain=args.min_split_gain,
        reg_alpha=args.reg_alpha,
        reg_lambda=args.reg_lambda,
        n_estimators=args.n_estimators,
        random_state=42,
    )

    # model.fit(X_train, y_train)

    model.fit(X_train, y_train, eval_set=[(X_val,y_val)], eval_metric="rmse", callbacks = [early_stopping(stopping_rounds=50, verbose=True)])

    model = XGBRegressor( 
            learning_rate=args.learning_rate,
            max_depth=args.max_depth,
            min_child_weight=args.min_child_weight,
            colsample_bytree=args.colsample_bytree,
            subsample=args.subsample,
            reg_alpha=args.reg_alpha,
            reg_lambda=args.reg_lambda,
            n_estimators=args.n_estimators,
            gamma=args.gamma,
            random_state=42,
            eval_metric="rmse", 
            early_stopping_rounds=50, 
            enable_categorical=True)


    model.fit(X_train, y_train, eval_set=[(X_val, y_val)],verbose = True)

    '''
    model = CatBoostRegressor( 
                learning_rate=args.learning_rate,
                depth=args.depth,
                l2_leaf_reg=args.l2_leaf_reg,
                random_strength=args.random_strength,
                border_count=args.border_count,
                subsample=args.subsample,
                rsm=args.rsm,
                min_data_in_leaf=args.min_data_in_leaf,
                iterations=args.iterations,
                random_state = 42, 
                loss_function="RMSE", 
                eval_metric="RMSE", 
                early_stopping_rounds=50,
                use_best_model=True)
    
    categorical_features = [
                                "item_id",
                                "dept_id",
                                "cat_id",
                                "store_id",
                                "state_id",
                                "event_name_1",
                                "event_type_1"
                            ]

    model.fit(X_train, y_train, cat_features = categorical_features, eval_set = [(X_val,y_val)],verbose = True)

    # During Trial 1  Suppose SageMaker chooses learning_rate = 0.05  num_leaves = 31
    # Then joblib.dump(model, model_path) saves /opt/ml/model/model.joblib on the EC2 instance running Trial 1.
    # When Trial 1 finishes, SageMaker automatically packages it as model.tar.gz and uploads it to S3.


    model_path = os.path.join(model_dir, "model.joblib")
    joblib.dump(model, model_path)
    # print(f"Model saved to: {model_path}")


    # predictions = model.predict(X_val, num_iteration = model.best_iteration_) # this is for Light GBM
    predictions = model.predict(X_val)
 
    #print(f"Best Iteration: {model.best_iteration_}") 

    rmse = root_mean_squared_error(y_val, predictions)

    print(f"validation:rmse={rmse}")


if __name__ == "__main__":
    main()


'''
best_estimator.hyperparameters()	Best hyperparameters
best_estimator.model_data	S3 path to the saved model (if one was saved)
best_estimator.latest_training_job.name	Best training job name
best_estimator.deploy()
'''

'''
With a SageMaker endpoint

When you execute:

predictor = best_estimator.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large"
)

SageMaker automatically:

Creates an EC2 instance.
Downloads your model.tar.gz from S3.
Loads the model into memory.
Starts a web server.
Exposes an HTTPS endpoint.
               Client
                  │
                  ▼
        HTTPS Request
                  │
                  ▼
      SageMaker Endpoint
                  │
        Loads LightGBM Model
                  │
                  ▼
           Prediction
                  │
                  ▼
         HTTPS Response
Example

Suppose your endpoint URL is:

https://runtime.sagemaker.us-east-1.amazonaws.com/endpoints/lightgbm-endpoint

Your application sends:

{
    "instances": [
        [12.5, 4, 30, 100],
        [15.2, 2, 18, 50]
    ]
}

The endpoint:

receives the request,
runs model.predict(),
returns:
{
    "predictions": [125.3, 142.7]
}

Your application never sees the model file—it just sends data and receives predictions.

Typical production architecture
               Web App
                   │
                   ▼
              REST API
                   │
                   ▼
          SageMaker Endpoint
                   │
                   ▼
            LightGBM Model
                   │
                   ▼
              Prediction
Do you need an endpoint?

For your demand forecasting project, probably not.

Your architecture is:

Hyperparameter Tuning
        │
        ▼
Best Hyperparameters
        │
        ▼
Train Final Model
        │
        ▼
Register in MLflow
        │
        ▼
FastAPI
        │
        ▼
POST /forecast

In this design:

FastAPI loads the model from MLflow (or local storage).
FastAPI exposes your own /forecast API.
You control authentication, logging, monitoring, and business logic.

This is a common approach when you already have an application server.

When would you use a SageMaker Endpoint?

You would deploy to a SageMaker endpoint if:

You don't want to build and manage your own FastAPI service.
You want AWS to manage scaling, availability, and infrastructure.
Other applications only need to call a prediction API hosted by AWS.

For your project, using MLflow + FastAPI is a good architectural choice because it gives you more flexibility and integrates well with the rest of your application.


'''