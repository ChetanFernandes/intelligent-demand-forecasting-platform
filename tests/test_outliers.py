from src_production_deployment.data_ingestion_processing.validation.outlier_validator import OutlierValidator
from src_production_deployment.data_ingestion_processing.validation.test_loader import call_data_loader
data = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")

outlier_validator = OutlierValidator()
outliers = outlier_validator.validate(data.sales)
print(outliers)