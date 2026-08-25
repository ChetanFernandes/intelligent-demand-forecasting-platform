from src_production_deployment.data_ingestion_processing.validation.great_exception_validation import GXValidator
from src_production_deployment.data_ingestion_processing.validation.test_loader import call_data_loader
data = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")

GX_validator = GXValidator()
results = GX_validator.validate(data.sales)
print(results)