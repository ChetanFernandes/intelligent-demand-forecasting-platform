from src_production_deployment.logger.logging import setup_logging
from src_production_deployment.data_ingestion_processing.validation.validation_report import ValidationReport
from src_production_deployment.configs.schema import EXPECTED_MISSING_COLUMNS
log = setup_logging()
import pandas as pd


class MissingValueValidator:

    def __init__(self):

        self.report = ValidationReport()

    def validate(self,df:pd.DataFrame, dataset_name:str,report: ValidationReport) -> None:
        
        ''' Checks if there is any missing values in Data'''
     
        missing_columns_count = df.isnull().sum()

        missing_columns = missing_columns_count[missing_columns_count > 0]

        if len(missing_columns) == 0:

            report.add_infm(f"No missing value found for dataset -> {dataset_name}")

            return

        total_rows = len(df)

        for column, count in missing_columns.items():

            percentage = (count / total_rows) * 100

            if column in EXPECTED_MISSING_COLUMNS:

                report.add_errors(
                                        f"[{dataset_name}] {column}: "
                                        f"{count} missing values ({percentage:.2f}%) - Expected."
                                    )

            else:

                report.add_errors(
                                        f"[{dataset_name}] {column}: "
                                        f"{count} missing values ({percentage:.2f}%)."
                                 )



  
                
