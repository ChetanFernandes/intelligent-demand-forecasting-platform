from src_production_deployment.data_ingestion_processing.feature_creation.calendar_join import CalendarJoiner
from src_production_deployment.data_ingestion_processing.feature_creation.reshape import SalesReshaper
from src_production_deployment.data_ingestion_processing.feature_creation.lag_feature import LagFeatureGenerator

from src_production_deployment.data_ingestion_processing.validation.test_loader import call_data_loader

data = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")

reshape = SalesReshaper()
Calendar_Joiner = CalendarJoiner()
lag_generator = LagFeatureGenerator()

sales_long = reshape.transform(data.sales)
merged = Calendar_Joiner.transform(sales_long, data.calendar)
lag_features = lag_generator.transform(merged)


print(lag_features[
        [
            "id",
            "date",
            "sales",
            "lag_1",
            "lag_7"
        ]

].head(15))

print(lag_features.shape)