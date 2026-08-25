from src_production_deployment.data_ingestion_processing.validation.schema_validator import SchemaValidator
from src_production_deployment.data_ingestion_processing.validation.test_loader import call_data_loader

data = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")

validator = SchemaValidator()
print(validator.validate(data.sales))

'''
Step 5.1 Schema Validation
Step 5.2 Missing Values
Step 5.3 Outliers
Step 5.4 Great Expectations
'''

