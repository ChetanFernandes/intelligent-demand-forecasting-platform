from src_production_deployment.data_ingestion_processing.feature_creation.calendar_join import CalendarJoiner
from src_production_deployment.data_ingestion_processing.feature_creation.reshape import SalesReshaper
from src_production_deployment.data_ingestion_processing.validation.test_loader import call_data_loader

data = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")

reshape = SalesReshaper()

Calendar_Joiner = CalendarJoiner()

sales_long = reshape.transform(data.sales)

print(sales_long.head())

print(sales_long.shape)

merged = Calendar_Joiner.transform(sales_long, data.calendar)

print(merged.head())

print(merged.shape)