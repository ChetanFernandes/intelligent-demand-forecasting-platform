from src_production_deployment.data_ingestion_processing.validation.validation_report import ValidationReport
from src_production_deployment.configs.schema import SALES_SCHEMA, CALENDAR_SCHEMA , SELL_PRICES_SCHEMA
from src_production_deployment.logger.logging import setup_logging
import pandas as pd
log = setup_logging()

class SchemaValidator:

    """ Schema validation for sales_train_validation_file"""

    def sales_train_validate(self, df:pd.DataFrame, report: ValidationReport ) -> None:

        required = SALES_SCHEMA["required_columns"]

        sales_prefix = SALES_SCHEMA["non_negative_prefixes"]

        sales_cols = [c for c in df.columns if c.startswith(sales_prefix)]

        missing = [c for c in required if c not in df.columns]

        if missing:

            report.add_errors(f" [Sales] Missing required columns : {missing}")

        elif not sales_cols:

            report.add_errors(f"No sales columns found (d_*)")

        if not missing and sales_cols:

            report.add_infm("Schema successfully validated for Sales Dataset")

    def calendar_validation(self,df:pd.DataFrame,report: ValidationReport) -> None:

        """ Schema validation for Calendar file"""

        required_columns = CALENDAR_SCHEMA["required_columns"]

        missing = [c for c in required_columns if c not in df.columns]

        if missing:

            report.add_errors(f" [Calendar] Missing required columns : {missing}")

        else:

            report.add_infm("Schema successfully validated for calendar Dataset")
   

    def sell_price_validator(self, df:pd.DataFrame,report: ValidationReport) -> None:
           
        """ Schema validation for sell price file"""

        required_columns = SELL_PRICES_SCHEMA["required_columns"]

        missing = [c for c in required_columns if c not in df.columns]

        if missing:

            report.add_errors(f"[Sellprice] Missing required columns : {missing}")

        else:

            report.add_infm("Schema successfully validated for sell price Dataset")
    
     



            




