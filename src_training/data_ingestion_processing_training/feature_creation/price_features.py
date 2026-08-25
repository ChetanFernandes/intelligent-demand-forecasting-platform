from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
import pandas as pd

class PriceFeatureGenerator:
    def transform(self,df:pd.DataFrame) -> pd.DataFrame :

        try:

            #print("ID column tpe", df["id"].dtype)

            #print("Type of columns itemid", df["item_id"].dtype)

            df = df.sort_values(by = ["item_id","store_id","wm_yr_wk"])

            grouped = df.groupby(["item_id","store_id"], observed = True)

            #df["price_change"] = grouped["sell_price"].transform(lambda x : x - x.shift(1)) # previous week price vs current week price
            
            df["price_change"] = grouped["sell_price"].diff()

            #df["price_pct_change"] = grouped["sell_price"].transform(lambda x : (x - x.shift(1)) / x.shift(1))

            df["price_pct_change"] = grouped["sell_price"].pct_change()

            df["discount_flag"] = (df["price_change"] < 0).astype(int) # 1 if price dropped.  0 otherwise

            log.info(f"Checking for null values -> {df[["sell_price", "price_change", "price_pct_change"]].isna().sum()}")

            log.info("cross checking unique (item_id, store_id) combinations: %s", df.groupby(["item_id", "store_id"]).ngroups)


            # Expected for first valid price in a group

            df["price_change"] = df["price_change"].fillna(0)

            df["price_pct_change"] = df["price_pct_change"].fillna(0)

            log.info("Number of rows having price_change as null post filling: %s", df["price_change"].isna().sum())

            log.info("Number of rows having price_pct_change as null post filling: %s", df["price_pct_change"].isna().sum())

            return df

        except Exception:
            log.exception("Error while generating columns related to price")
            raise

