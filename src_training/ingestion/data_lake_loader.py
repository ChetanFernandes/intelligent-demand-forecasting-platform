import pandas as pd
from src_production_deployment.data_ingestion_processing.ingestion.data_lake_reader import DataLakeReader
from src_production_deployment.data_ingestion_processing.ingestion.contracts import ForecastDataset
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()

class DataLoader:

    def __init__(self,account_name:str, filesystem:str):

        log.info("Initializing DataLoader")

        self.reader = DataLakeReader(account_name=account_name, filesystem=filesystem)

    
    def load(self) -> ForecastDataset:
        """ Read the file from ADLS and store in memory"""

        log.info("Inside function to load data from ADLS")

        try:
      
            sales = pd.read_csv(self.reader.read_file("raw/sales/sales_train_evaluation.csv"))
            log.info("sales_train_validation file successfully loaded")

            calendar = pd.read_csv(self.reader.read_file("raw/calendar/calendar.csv"))
            log.info("calendar file successfully loaded")

            prices = pd.read_csv(self.reader.read_file("raw/prices/sell_prices.csv"))
            log.info("selling price file successfully loaded")

            return ForecastDataset(sales=sales,calendar=calendar,prices=prices)
        
        except Exception:
            log.exception("File loading from Azure failed")
            raise

    





