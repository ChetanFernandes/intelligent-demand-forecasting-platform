import pandas as pd
from logger.logging import setup_logging
log = setup_logging()


def load_data():
    try:
        X_train = pd.read_parquet(r"artifacts\datasets\data_split\X_train.parquet")
        Y_train = pd.read_parquet(r"artifacts\datasets\data_split\Y_train.parquet")

        X_val = pd.read_parquet(r"artifacts\datasets\data_split\X_val.parquet")
        Y_val = pd.read_parquet(r"artifacts\datasets\data_split\Y_val.parquet")

        #print("Mean Sales :", Y_val.mean())
        #print("Median Sales :", Y_val.median())
        #print("Std Dev :", Y_val.std())
        #print("Min Sales :", Y_val.min())
        #print("Max Sales :", Y_val.max())
        #print((Y_val == 0).mean())
        #print((Y_val["sales"] == 0).mean())

        return X_train, Y_train, X_val, Y_val
    
    except Exception:
        log.exception("Data Load failed")


def load_data_hyper():
    try:
        X_train = pd.read_parquet(r"artifacts\datasets\data_split\X_train.parquet")
        Y_train = pd.read_parquet(r"artifacts\datasets\data_split\Y_train.parquet")
        #X_val = pd.read_parquet(r"artifacts\datasets\data_split\X_val.parquet")
        #y_val = pd.read_parquet(r"artifacts\datasets\data_split\Y_val.parquet")

        #print("Mean Sales :", Y_val.mean())
        #print("Median Sales :", Y_val.median())
        #print("Std Dev :", Y_val.std())
        #print("Min Sales :", Y_val.min())
        #print("Max Sales :", Y_val.max())
        #print((Y_val == 0).mean())
        #print((Y_val["sales"] == 0).mean())

        return X_train, Y_train
    
    except Exception:
        log.exception("Data Load failed")