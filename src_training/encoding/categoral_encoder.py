# 1. Tell LightGBM these are categorical features. Since we are using LightGBM model we have to convert category columns to type category and it
# dont work on str or object
# 2. Reduce memory usage

class CategoricalEncoder:

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

    def transform(self, df):

        df = df.copy()

        for col in self.categorical_columns:
            df[col] = df[col].astype("category")

        return df
    
#LightGBM + Native Categories
#vs
#LightGBM + Target Encoding
#Model 1
##--------
#LightGBM
#Native Categories

#Model 2
#--------
#LightGBM
#Target Encoding

#Model 3
#--------
#ARIMA

#Model 4
#--------
#SARIMA

#Model 5
#--------
#Prophet