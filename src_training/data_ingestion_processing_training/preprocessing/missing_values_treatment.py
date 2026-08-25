import pandas as pd
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
from configs.schema import EXPECTED_MISSING_COLUMNS

class FillMissingValue:

    def values(self,df:pd.DataFrame) -> pd.DataFrame:

        try:

            before_name = df["event_name_1"].isna().sum()
            before_type = df["event_type_1"].isna().sum()
  


            for c in EXPECTED_MISSING_COLUMNS:
                if c in df.columns:
                    df[c] = df[c].fillna("No_Event")

            
            after_name = df["event_name_1"].isna().sum()
            after_type = df["event_type_1"].isna().sum()

            #df.to_parquet("artifacts/recursive_prediction/calendar_processed.parquet")
            #df.to_csv("artifacts/recursive_prediction/calendar_processed.csv")

            log.info(
                f"Filled expected missing values. "
                f"event_name_1: {before_name} -> {after_name}, "
                f"event_type_1: {before_type} -> {after_type}"
            )

        except Exception as e:
            log.exception(f"Unexpected error occured while filling missing value for column {c} : {e}")
        
        
     

        
