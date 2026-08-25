class TargetCategoryEncoder:

    def __init__(self):

        self.categorical_columns = [
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id",
            "event_name_1",
            "event_type_1"
        ]

        self.mappings = {}
        
        self.global_mean = None


    def fit_transform(self, X_train, y_train):

        X_train = X_train.copy()

        if hasattr(y_train,"squeeze"):
            y_train = y_train.squeeze()

        self.global_mean = y_train.mean()


        for col in self.categorical_columns:
    
            # Compute target mean for each category
            mapping = y_train.groupby(X_train[col], observed=True).mean().astype("float32")

            self.mappings[col] = mapping
    
            # Apply encoding
            X_train[col] = X_train[col].astype(str).map(mapping).fillna(self.global_mean).astype("float32")


        
        return X_train

    def transform(self,X):

        X = X.copy()

        for col in self.categorical_columns:

            X[col] = (X[col].astype(str).map(self.mappings[col]).fillna(self.global_mean).astype("float32"))

        return X
