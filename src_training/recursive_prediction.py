from src_production_deployment.data_ingestion_processing.main import DataLoader
from src_production_deployment.data_ingestion_processing.validation.schema import ValidationError
from configs.project_config import AZURE_ACCOUNT_NAME , AZURE_FILESYSTEM
from src_production_deployment.data_ingestion_processing.validation.validation_report import ValidationReport
from src_production_deployment.production_deployment.champion_model_download import champion_model_download
from src_training.registry.mlflow_registry import ModelRegistry
import pandas as pd
from pathlib import Path
import numpy as np
from src_production_deployment.data_ingestion_processing.feature_creation.calendar_join import CalendarJoiner
from logger.logging import setup_logging
log = setup_logging()


class RecursivePrediction:

    def __init__(self):

        self.calendar_joiner = CalendarJoiner()

        self.path = Path("artifacts/recursive_prediction/")
        
        self.path.mkdir(parents=True, exist_ok=True)

        self.loader = DataLoader(account_name = AZURE_ACCOUNT_NAME, filesystem = AZURE_FILESYSTEM)

        self.prediction = champion_model_download(registry = ModelRegistry(), splitter = None, evaluator=None)

        log.info("All files successfully loaded")

    def data_validation(self):

        report = ValidationReport()

        self.loader.data_validation(report) 

        report_path = report.save_report_first_validation()

        if report.has_errors():

            log.warning(f"Initial validation found issues. "
                        f"Report saved at: {report_path}"
                        )


            # Try to fix the issues
            self.loader.data_preprocessing()

            # Re-validation
            report = ValidationReport()

            self.loader.data_re_validation(report)

            report_path = report.save_report_re_validation()

            if report.has_errors():

                raise ValidationError(
                    f"Validation failed after preprocessing. "
                    f"Report saved at: {report_path}"
                )

            else:
                log.info("No errors reported during second validation.Proceeding with Data Massage")
                pass


        else:
            log.info("No errors reported during first validation.Proceeding with Data Massage")
            pass

    def da_massaging(self, path):

        self.loader.data_massaging(path)

        log.info("Sales_evaluation_reshaped and extracting unique item'ids completed")

   
    def recursive_prediction(self, path:str, forecast_days:int) -> pd.DataFrame:
        
        sales_reshaped = pd.read_parquet(path/"sales_reshaped.parquet")

        future_rows_unique = pd.read_parquet(path/"future_rows_unique.parquet")

        last_day  = sales_reshaped["day"].str.extract(r"(\d+)")[0].astype(int).max()

        day = last_day + 1

        prediction_days = last_day + forecast_days
        1944 = 1941 + 3

        combined = None

        while (day <= prediction_days):

            future_rows = future_rows_unique.copy()

            prediction_day = f"d_{day}"

            log.info("prediction for day \n%s",
                      prediction_day)

            future_rows["day"] = prediction_day

            future_rows["sales"] = np.nan

            log.info("future_rows_unique shape post adding two new columns %s ", future_rows.shape)

            recursive_result, combined  = self.recurrsive_tasks(sales_reshaped, future_rows, prediction_day, combined)

            combined = self.post_prediction_single_day(recursive_result, combined, future_rows, prediction_day)

            log.info("prediction completed for day \n%s",
                      prediction_day)

            combined.to_csv(path/f"combined_{prediction_day}.csv")
            
            log.info("sales updated in combined report")
            
            day = day + 1

        log.info(f"Prediction for {forecast_days} completed")

        day_number = combined["day"].str.extract(r"(\d+)")[0].astype(int)
        # .str.extract(r"(\d+)") - This uses a regular expression to extract the digits.
        # (\d+) - \d → a digit (0–9) , + → one or more digits, ( ) → capture that part

        result = combined.loc[day_number.between(last_day + 1, prediction_days)].copy

        log.info("Final Result \n%s",
                 result)

        return result

if __name__ == "__main__":
    recursive_prediction = RecursivePrediction()
    recursive_prediction.data_validation()
    recursive_prediction.da_massaging(recursive_prediction.path)
    recursive_prediction.recursive_prediction(recursive_prediction.path)

