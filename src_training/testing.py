import pandas as pd
X_inference = pd.read_parquet(r"artifacts/production/X_inference.parquet")
#Y_inference = pd.read_parquet(r"artifacts/production/Y_inference.parquet")
#X_test = pd.read_parquet(r"artifacts/datasets/data_split/X_test.parquet")
#Y_test = pd.read_parquet(r"artifacts/datasets/data_split/Y_test.parquet")
#X_val = pd.read_parquet(r"artifacts/datasets/data_split/X_val.parquet")
X_train = pd.read_parquet(r"artifacts/datasets/train_df.parquet")

#features = pd.read_csv(r"artifacts/production/features_final.csv")

#features[:300000].to_csv("artifacts/production/features_final.csv")
#features[-20:].to_csv("artifacts/production/features_final_1.csv")

print("Training event_name_1:")
print(X_train["event_name_1"].isna().sum())

print(
    X_train["event_name_1"]
    .value_counts(dropna=False)
    .tail()
)


print("Training event_type_1:")
print(X_train["event_type_1"].isna().sum())

print(
    X_train["event_type_1"]
    .value_counts(dropna=False)
    .tail()
)

'''
print("X_inference:", X_inference.shape)
print("Y_inference:", Y_inference.shape)

print("\nX index:")
print(X_inference.index[:10])

print("\nY index:")
print(Y_inference.index[:10])

print("Same number of rows:",
      len(X_inference) == len(Y_inference))


print("Inference year:")
print(X_inference["year"].value_counts().sort_index())

print("\nInference week range:")
print(
    X_inference["wm_yr_wk"].min(),
    X_inference["wm_yr_wk"].max()
)

print("\nSales statistics:")
print(Y_inference["sales"].describe())

print("X_test years:")
print(X_test["year"].value_counts().sort_index())

print("\nX_test week range:")
print(
    X_test["wm_yr_wk"].min(),
    X_test["wm_yr_wk"].max()
)

print("\nY_test sales statistics:")
print(Y_test["sales"].describe())



print("X_inference shape:", X_inference.shape)
print("X_inference columns:", X_inference.columns.tolist())

print("\nX_inference dtypes:")
print(X_inference.dtypes)

print("X_test shape:", X_test.shape)
print("X_test columns:", X_test.columns.tolist())

print("\nX_test dtypes:")
print(X_test.dtypes)
'''












'''

col = X_test.columns[9]

print("Columns",col)


print("\nTRAIN:")
print("dtype:", X_test[col].dtype)

if str(X_train[col].dtype) == "category":
    print("categories:", X_train[col].cat.categories.tolist())

print("\nVALIDATION:")

print("dtype:", X_val[col].dtype)

if str(X_val[col].dtype) == "category":
    print("categories:", X_val[col].cat.categories.tolist())

print("\nINFERENCE:")

print("dtype:", X_test[col].dtype)

if str(X_test[col].dtype) == "category":
    print("categories:", X_test[col].cat.categories.tolist())

col = X_test.columns[9]
print(X_test.loc[X_test[col].isin(["OrthodoxEaster", "Pesach End"]),col].value_counts())
print(X_test[col].isin(["OrthodoxEaster", "Pesach End"]).sum())
'''