
from configs.project_config import TRAIN_SAMPLE_SIZE, RANDOM_STATE

def preprocess_data(X_train, Y_train, X_val):

    categorical_columns = [
        "item_id",
        "dept_id",
        "cat_id",
        "store_id",
        "state_id",
        "event_name_1",
        "event_type_1"
    ]


    X_train_sample = X_train.sample(n=TRAIN_SAMPLE_SIZE, random_state=RANDOM_STATE)

    y_train_sample = Y_train.loc[X_train_sample.index]

    #print(X_train_sample[categorical_columns].isnull().sum())

    #print(X_val[categorical_columns].isnull().sum())

    for col in categorical_columns:
        X_train_sample[col] = (
            X_train_sample[col]
            .astype("string")
            .fillna("Unknown")
        )

        X_val[col] = (X_val[col].astype("string").fillna("Unknown"))


    return X_train_sample, y_train_sample, X_val