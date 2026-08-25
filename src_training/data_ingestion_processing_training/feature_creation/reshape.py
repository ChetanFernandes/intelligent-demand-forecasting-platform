from configs.schema import SALES_SCHEMA
from configs.project_config import LOOKBACK_DAYS
import pandas as pd
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()

class SalesReshaper:
    def transform(self,df:pd.DataFrame) -> pd.DataFrame :
        try:

            cat_columns = SALES_SCHEMA["required_columns"]

            sales_columns = [column for column in df.columns if column.startswith(SALES_SCHEMA["non_negative_prefixes"])][-28:]
            log.info("Sales columns selected for recursive history: %s", sales_columns)

            reshaped = df.melt(id_vars = cat_columns, value_vars = sales_columns, var_name = "day", value_name = "sales")

            # id_vars - columns shd remain unchnaged
            # value_vars - These columns shd be unpivoted. Covert them from columns to rows
            # var_name - When Pandas converts column names into rows, it needs a column to store those original column names.
            # value_name - to store the value of column day
            
            #log.info(f"After melt ,{reshaped["day"].min()}")

            reshaped[cat_columns] = reshaped[cat_columns].astype("category")
            
            reshaped["sales"] = reshaped["sales"].astype("int16")

            future_rows_unique = reshaped[["id", "item_id", "dept_id", "cat_id", "store_id", "state_id"]].drop_duplicates()

            return reshaped , future_rows_unique

        except Exception:
                log.exception("Error_while_converting_columns to row")
                raise

   
                 
    
