from src_training.encoding.Target_encoding import TargetCategoryEncoder
from configs.project_config import TRAIN_SAMPLE_SIZE, RANDOM_STATE
import pandas as pd

def preprocess_data(X_train,Y_train,X_val):

    encoder = TargetCategoryEncoder()

    #X_train_sample = X_train.sample(n=5000000, random_state=RANDOM_STATE)

    #y_train_sample = Y_train.loc[X_train_sample.index]

    X_train  = encoder.fit_transform(X_train,Y_train)
    
    X_val = encoder.transform(X_val)

    return X_train , Y_train, X_val







