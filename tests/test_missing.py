from src_production_deployment.data_ingestion_processing.validation.missing_values_validator import MissingValueValidator
from src_production_deployment.data_ingestion_processing.validation.test_loader import call_data_loader

data = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")

missing_validator = MissingValueValidator()

print(missing_validator.validate(data.sales))