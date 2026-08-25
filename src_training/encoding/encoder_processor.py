from src_training.encoding.categoral_encoder import CategoricalEncoder
from configs.project_config import TRAIN_SAMPLE_SIZE, RANDOM_STATE
from src_training.encoding.Target_encoding import TargetCategoryEncoder



def preprocess_data_hyper_native(X_train, Y_train):

    encoder = CategoricalEncoder() #convert column to type category

    X_train = encoder.transform(X_train)

    X_train_sample = X_train.sample(n=TRAIN_SAMPLE_SIZE, random_state=RANDOM_STATE)

    y_train_sample = Y_train.loc[X_train_sample.index]

    return  X_train_sample, y_train_sample

def preprocess_data_hyper_target(X_train,Y_train):

    encoder = TargetCategoryEncoder() # Target encoding

    X_train_sample = X_train.sample(n=TRAIN_SAMPLE_SIZE, random_state=RANDOM_STATE)

    y_train_sample = Y_train.loc[X_train_sample.index]

    X_train_sample  = encoder.fit_transform(X_train_sample,y_train_sample)

    return X_train_sample , y_train_sample


def preprocess_data_test_native(X_train, Y_train, X_val):

    encoder = CategoricalEncoder() # Convert column to type category

    X_train_sample = X_train.sample(n=TRAIN_SAMPLE_SIZE , random_state=RANDOM_STATE)

    y_train_sample = Y_train.loc[X_train_sample.index]

    X_train = encoder.transform(X_train_sample)

    X_val = encoder.transform(X_val)

    #X_train_sample = X_train.sample(random_state=RANDOM_STATE)

    #y_train_sample = Y_train.loc[X_train_sample.index]

    return X_train, X_val , y_train_sample


def preprocess_data_test_target(X_train, X_val, y_train):

    encoder = TargetCategoryEncoder() # Taregt encodinh

    X_train  = encoder.fit_transform(X_train,y_train)

    X_val = encoder.transform(X_val)

    return X_train , X_val