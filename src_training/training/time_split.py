
'''
1. Drop rows with missing lag/rolling features
2. Last 28 days = Test
3. Everything before = Train
4. Separate X and y
'''

import pandas as pd
from logger.logging import setup_logging
log = setup_logging()

class TimeSeriesSplitter:
    
    def split(self,df:pd.DataFrame, validation_days = 28, test_days = 28) -> pd.DataFrame:

        try:
        
            log.info(f"shape_before_dropna -  {df.shape}")

            log.info(f"Min day before dropping null rows -> {df["day"].min()}")

            log.info(f"Dropping rows having null values from columns  lag_28, rolling_mean_28, rolling_std_7")

            required_features = [
                                    "lag_28",
                                    "rolling_mean_28",
                                    "rolling_std_7"
                                ]

            df = df.dropna(subset=required_features) # this removes the rows for which above columns are nill

            log.info(f"shape_after_dropna - {df.shape}")
            
            log.info(f"Min day after dropping null rows {df["day"].min()}")

            log.info("Number of rows having price_change as null: %s", df["price_change"].isna().sum())

            log.info("Number of rows having price_pct_change as null: %s", df["price_pct_change"].isna().sum())

            df["price_change"] = df["price_change"].fillna(0)

            df["price_pct_change"] = df["price_pct_change"].fillna(0)

            log.info("Number of rows having price_change as null post filling : %s", df["price_change"].isna().sum())

            log.info("Number of rows having price_pct_change as null post filling : %s", df["price_pct_change"].isna().sum())

            df = df.sort_values("date").reset_index(drop=True)

            max_date = df["date"].max()

            log.info("Max_date: %s", max_date)

            test_start  = max_date - pd.Timedelta(days = test_days-1) # to specify unit (days/week/month) we use pd.Timedelta

            log.info("test_start: %s", test_start)

            #test_start - finds the first day of that 28-day window.

            validation_start = test_start - pd.Timedelta(days = validation_days)

            log.info(f"validation_start, {validation_start}")

            train_df = df[df["date"] < validation_start]

            validation_df = df[(df["date"] >= validation_start) & (df["date"] < test_start)]

            test_df = df[df["date"] >= test_start]

            return train_df, test_df, validation_df

        except Exception:
            log.exception("Error occured while splitting data to train, valid and test")
            raise
        

