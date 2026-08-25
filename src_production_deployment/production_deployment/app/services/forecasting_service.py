from src_production_deployment.production_deployment.recursive_prediction_aws import RecursivePredictionAws
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()

class ForecastingService:

    def __init__(self):

        self.recursive_prediction = RecursivePredictionAws()

        log.info("Application successfully started")

        #self.recursive_prediction.move_data_to_s3()
        #log.info("All files loaded to s3")
        
        #self.recursive_prediction.move_champion_model_to_s3()
        
        #log.info("Model loaded to s3")

        self.recursive_prediction.prepare()


    def forecast(self,forecast_days:int) -> dict:

        try:

            if forecast_days <= 0:
                raise ValueError("Forecast_days must be greater than 0")
            
            log.info("Forecast request received: forecast_days = %s", forecast_days)

            result = self.recursive_prediction.predict(forecast_days)

            log.info("Forecast completed successfully: forecast_days=%s", forecast_days)

            '''
            return {  
                    "forecast_days" : forecast_days,
                    "predictions" : result.to_dict(orient = "records") # Convert my DataFrame into a list where every row is represented as a dictionary.
                    }
            '''
            return {
                     "forecast_days" : forecast_days,
                      "predictions" : result

            }

        except Exception as e:
            log.exception(str(e))
            raise  # FastAPI handles the exception


'''
ForecastingService
        │
        │ forecast_days
        ▼
RecursivePrediction
        │
        ├── owns forecasting path
        ├── owns DataLoader
        ├── owns model
        └── owns recursive logic
'''