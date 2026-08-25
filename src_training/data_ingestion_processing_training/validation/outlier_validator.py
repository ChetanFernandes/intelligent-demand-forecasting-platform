from configs.schema import SALES_SCHEMA
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
from src_production_deployment.data_ingestion_processing.validation.validation_report import ValidationReport
import pandas as pd
from pathlib import Path
from datetime import datetime

class OutlierValidator:

    def validate(self, df:pd.DataFrame, dataset_name:str, report: ValidationReport,path) -> None:

        if dataset_name != "sales":

            return
            
        sales_columns = [column for column in df.columns if column.startswith(SALES_SCHEMA["non_negative_prefixes"])]

        sales_data = df[sales_columns]

        #flattened = sales_data.values.flatten() # converts that 2D array into a 1D array.

        #flattened = flattened[flattened > 0]
        
        #log.info(f"Flattened shape: {flattened.shape}")

        stacked = sales_data.stack() #this give row details

        stacked = stacked[stacked > 0]

        outliers = []

        q1 = stacked.quantile(0.25)

        q3 = stacked.quantile(0.75)

        iqr = q3 - q1

        lower = (q1 - 1.5 * iqr)
        upper = (q3 + 1.5 * iqr)

        for (row, column), value in stacked.items():

            if value < lower or value > upper:

                outliers.append({
                    "row": row,
                    "column": column,
                    "value": value
                })

        outlier = pd.DataFrame(outliers)
        
        outlier.insert(0, "dataset", dataset_name)
 
        path = Path(path/f"validation_report")

        path.mkdir(parents=True,exist_ok=True)

        filename = (
                    f"outlier_report_"
                    f"{datetime.now():%Y%m%d_%H%M%S}.csv"
                )
        
        outlier.to_csv(path/filename,index=False)

        if len(outliers) > 0:

            report.add_warnings(f" Detected {len(outliers)} outliers in dataset '{dataset_name}' ")
            
        else: 

            report.add_infm(f"No outliers detected in dataset '{dataset_name}'.")



     
        
      

