from src_production_deployment.data_ingestion_processing.feature_creation.calendar_join import CalendarJoiner
from src_production_deployment.data_ingestion_processing.feature_creation.reshape import SalesReshaper
from src_production_deployment.data_ingestion_processing.feature_creation.lag_feature import LagFeatureGenerator
from src_production_deployment.data_ingestion_processing.feature_creation.rolling_features import RollingFeatureGenerator

from src_production_deployment.data_ingestion_processing.validation.test_loader import call_data_loader

data = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")

reshape = SalesReshaper()
Calendar_Joiner = CalendarJoiner()
lag_generator = LagFeatureGenerator()
rolling_generator = RollingFeatureGenerator()

sales_long = reshape.transform(data.sales)
print(sales_long.head(10))
merged = Calendar_Joiner.transform(sales_long, data.calendar)
print(merged.head(10))
lag_features = lag_generator.transform(merged)
print(lag_features.head(10))
rolling_features = rolling_generator.transform(lag_features)

print(rolling_features[
        [
            "id",
            "date",
            "sales",
            "lag_1",
            "lag_7",
            "rolling_mean_7",
            "rolling_std_7"

        ]

].head(15))

print(lag_features.shape)