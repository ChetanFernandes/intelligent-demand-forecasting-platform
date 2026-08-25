from src_production_deployment.data_ingestion_processing.validation.schema import ValidationError
import pandas as pd
from pathlib import Path
import numpy as np
from src_production_deployment.production_deployment.utilis.repeat_code import recurrsive_tasks, post_prediction_single_day
from src_production_deployment.production_deployment.data_loader import DataLoader
from src_production_deployment.data_ingestion_processing.validation.validation_report import ValidationReport
from src_production_deployment.production_deployment.s3.s3_manager import S3Manager
from src_production_deployment.production_deployment.aws_session_prod import AWSSession
from io import BytesIO
from src_production_deployment.production_deployment.sagemaker.predictor import SageMakerPredictor
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()



class RecursivePredictionAws:

    def __init__(self):
        
        self.path = Path("artifacts/recursive_prediction/")

        self.path.mkdir(parents=True, exist_ok=True)

        self.loader = DataLoader()

        self.s3_manager = S3Manager(AWSSession())

        self.calendar =  self.s3_manager.read_file(s3_key = "forecast_data/calendar.parquet")
                
        self.sell_price =  self.s3_manager.read_file(s3_key = "forecast_data/sell_price.parquet")

        self.predictor = SageMakerPredictor(endpoint_name="demand-forecasting-endpoint-endpoint-v6", region_name="us-east-1")


    '''
    def move_data_to_s3(self):
        self.loader.load_to_s3_calendar("calendar")
        self.loader.load_to_s3_sell_price("sell_price")
        log.info("Files loaded to s3 successfully")

    def move_champion_model_to_s3(self):
        artifact_path = r"mlruns/664241320219745211/models/m-ec3e5a4f517f43f0a883464382aea3b5/artifacts"
        self.loader.load_champion_model_s3(artifact_path)
        log.info("Model successsfully loded to s3")
    '''

        
    def prepare(self):

        self.data_validation()

        '''
        sales_reshaped_path = self.path / "sales_reshaped.parquet"
        future_rows_path = self.path / "future_rows_unique.parquet"

        if not sales_reshaped_path.exists() or not future_rows_path.exists():
            self.da_massaging(self.path)

        if not sales_reshaped_path.exists():
            raise FileNotFoundError(f"Required artifact not found: {sales_reshaped_path}")

        if not future_rows_path.exists():
            raise FileNotFoundError(f"Required artifact not found: {future_rows_path}")
        '''

    def data_validation(self):
    
        report = ValidationReport()

        self.loader.data_validation(report, self.calendar, self.sell_price, self.path) 

        report_path = report.save_report_first_validation(self.path)

        if report.has_errors():

            log.warning(f"Initial validation found issues. "
                        f"Report saved at: {report_path}"
                        )


            # Try to fix the issues
            self.loader.data_preprocessing(self.calendar)

            # Re-validation
            report = ValidationReport()

            self.loader.data_re_validation(report, self.calendar)

            report_path = report.save_report_re_validation(self.path)

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

    '''
    def da_massaging(self, path):

        self.loader.data_massaging(path)

        log.info("Sales_evaluation_reshaped and extracting unique item'ids completed")
    '''
    
  

    def predict(self, forecast_days: int):

        return self.recursive_prediction(self.path, forecast_days)

    def recursive_prediction(self, path:str, forecast_days:int) -> pd.DataFrame:
        
        sales_reshaped = self.s3_manager.read_file(s3_key = "forecast_data/sales_reshaped.parquet")
        future_rows_unique = self.s3_manager.read_file(s3_key = "forecast_data/future_rows_unique.parquet")

        last_day  = sales_reshaped["day"].str.extract(r"(\d+)")[0].astype(int).max()

        day = last_day + 1

        prediction_days = last_day + forecast_days

        combined = None

        while (day <= prediction_days):

            future_rows = future_rows_unique.copy()

            prediction_day = f"d_{day}"

            log.info("prediction for day \n%s",
                        prediction_day)

            future_rows["day"] = prediction_day

            future_rows["sales"] = np.nan

            log.info("future_rows_unique shape post adding two new columns %s ", future_rows.shape)

        
            recursive_result, combined  = recurrsive_tasks(sales_reshaped, future_rows, prediction_day, path, self.loader, self.calendar, self.sell_price, self.predictor, combined) 

            combined = post_prediction_single_day(recursive_result, combined, future_rows, prediction_day)

            log.info("prediction completed for day \n%s",
                        prediction_day)

            combined.to_csv(path/f"combined_{prediction_day}.csv")
            
            log.info("sales updated in combined report")
            
            day = day + 1

        log.info(f"Prediction for {forecast_days} completed")

        day_number = combined["day"].str.extract(r"(\d+)")[0].astype(int)
        # .str.extract(r"(\d+)") - This uses a regular expression to extract the digits.
        # (\d+) - \d → a digit (0–9) , + → one or more digits, ( ) → capture that part

        result = combined.loc[day_number.between(last_day + 1, prediction_days)].copy()

        result = result.drop(columns="d").reset_index(drop=True)

        buffer = BytesIO()

        result.to_csv(buffer,index = False)

        # Reset buffer position
        buffer.seek(0)

        # upload to S3
        self.s3_manager.upload_file_memory(buffer,key = "forecast_result/result.csv")

        return result
