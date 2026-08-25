from src_production_deployment.data_ingestion_processing.ingestion.data_lake_loader import DataLoader
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
import pandas as pd

def call_data_loader(account_name, filesystem):

    try:

        loader = DataLoader(account_name=account_name, filesystem=filesystem)

        dataset = loader.load()

        log.info("Sales_evaluation_csv_file_shape: %s", dataset.sales.shape)
        log.info("Calendar_csv_file_shape: %s ",dataset.calendar.shape)
        log.info("Price_csv_file_shape: %s",    dataset.prices.shape)

        return dataset

    except Exception:
           log.exception("Failed to load datasets")
           raise

      
'''
if __name__ == "__main__":

    dataset = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")
'''

