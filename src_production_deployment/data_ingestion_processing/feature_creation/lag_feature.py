import pandas as pd
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()

class LagFeatureGenerator:
    """Models learn temporal patterns through lag features."""
    ''' A lag feature means: Past value used as input for predicting future value'''
    
    def transform(self,df:pd.DataFrame) -> pd.DataFrame:

        try: 

            convert_to_categorical_columns = [
                        "d",
                        "weekday",
                        "event_name_1",
                        "event_type_1",
                        "event_name_2",
                        "event_type_2",
                    ]

            #Other columns ("id","item_id","dept_id",'cat_id','store_id','state_id') are already categorical
            
            for col in convert_to_categorical_columns:
                
                df[col] = df[col].astype("category")

            df["date"] = pd.to_datetime(df["date"])

            df = df.sort_values(["id", "date"], kind="mergesort")

            grouped = df.groupby("id", observed = True)

            df["lag_1"] = grouped["sales"].shift(1)
            df["lag_7"] = grouped["sales"].shift(7)
            df["lag_28"] = grouped["sales"].shift(28)

            #print(df.memory_usage(deep=True))
            return df

        except Exception:
            log.exception("Error while generationg lag column")
            raise

'''
1. shift(1)
    day	  sales	   lag_1
    1	   10	    null
    2	   15	     10
    3	   20	     15


2. groupby("id")
   Means: Create lag separately for each product-store .


3. Why sort is critical

Without:

sort_values()

lags become meaningless.

Because temporal order breaks.

Very important production detail.
'''