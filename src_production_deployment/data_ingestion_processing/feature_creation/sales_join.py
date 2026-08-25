from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
import pandas as pd


class PriceJoiner:
    def transform(self,sales_df:pd.DataFrame,prices_df:pd.DataFrame) -> pd.DataFrame:
        try:

            
            convert_to_categorical_columns = [
                                    "item_id",
                                    "store_id",
                                ]
            
            for col in convert_to_categorical_columns:
                prices_df[col] = prices_df[col].astype("category")
 
            print("Sales item_id :", sales_df["item_id"].dtype)
            print("Prices item_id:", prices_df["item_id"].dtype)
    
            print("Sales store_id :", sales_df["store_id"].dtype)
            print("Prices store_id:", prices_df["store_id"].dtype)

        
            merged = sales_df.merge(prices_df, on=["item_id","store_id","wm_yr_wk"], how = "left")
            
            log.info("Object columns after PriceJoiner: %s",merged.select_dtypes(include="object").columns.tolist())

            log.info(f"DataFrame shape after merging -> {merged.shape}")
                        
            log.info(f"DataFrame having rows with selling price as Null -> {merged['sell_price'].isna().sum()}")

            sales_column_with_missing_price = merged.loc[merged["sell_price"].isna(),"sales"] 

            # give series where sales
            # checks every row of sell_price column and you get boolean series
            # merged.loc[...] .lets you select: Select the sales column only for rows where sell_price is missing.

            #print(sales_column_with_missing_price[:10])

            selling_price_missing = merged[merged["sell_price"].isna()].copy()

            #print(selling_price_missing[:10])

            #.loc selects using labels or conditions. .iloc selects using integer positions.
            #  merged.iloc[1, 2] - Give me the value at row position 1, column position 2.
            # merged.iloc[1:4, 2] - Give me rows at positions 1 through 3 from column position 2.

    
            log.info("Rows with missing sell_price: %s", len(sales_column_with_missing_price))

            log.info("Sales statistics for rows with missing sell_price:\n%s", sales_column_with_missing_price.describe())

            log.info("Rows with sales > 0 and missing sell_price: %s", (sales_column_with_missing_price > 0).sum()) 
            #pandas applies this to every element in series


            log.info(f"{sales_column_with_missing_price.value_counts().head(10)}") 

            # From the rows where sell_price is NaN, return only the sales column."
            # .valuecounts - Counts how many times each sales value occurs.


            log.info("Dropping rows with missing sell_price")

            merged = merged.dropna(subset=["sell_price"])

            log.info(f"DataFrame shape after merging post dropping missing selling price values-> {merged.shape}")
                                    
            log.info(f"DataFrame having rows with selling price as Null post dropping-> {merged['sell_price'].isna().sum()}")


            # Find first row with missing sell_price
            '''
            missing = merged[merged["sell_price"].isna()].iloc[0] # Give me the first row by position. It returns series

            print("Item:", repr(missing["item_id"]))
            print("Store:", repr(missing["store_id"]))
            print("Week:", repr(missing["wm_yr_wk"]))

            print(missing["item_id"] in prices_df["item_id"].unique())
            print(missing["store_id"] in prices_df["store_id"].unique())
            
            # Verify whether this combination exists in sell_prices.csv
            print(
                prices_df[
                    (prices_df["item_id"] == missing["item_id"]) &
                    (prices_df["store_id"] == missing["store_id"]) &
                    (prices_df["wm_yr_wk"] == missing["wm_yr_wk"])
                ]
            )
            '''
            return merged , selling_price_missing , sales_column_with_missing_price
        
        except Exception:
            log.exception("Error while merging sales and price file")
            raise

'''
Why how="left"?

We always want to keep:

Sales rows

because sales is our primary dataset.

If some price is missing:

sell_price = NaN

but we don't lose the sales observation.

This is standard forecasting practice.
'''