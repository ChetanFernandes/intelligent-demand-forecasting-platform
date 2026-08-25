# 1. Tell LightGBM these are categorical features
# 2. Reduce memory usage

from src_training.encoding.categoral_encoder import CategoricalEncoder
import pandas as pd

encoder = CategoricalEncoder()

X_train = pd.read_parquet(r"artifacts\datasets\X_train.parquet")
X_test = pd.read_parquet(r"artifacts\datasets\X_test.parquet")

print(X_train.shape)
print(X_test.shape)

X_train = encoder.transform(X_train)
X_test = encoder.transform(X_test)


print(X_train.dtypes)
