from src_production_deployment.data_ingestion_processing.feature_creation.calendar_join import CalendarJoiner
from src_production_deployment.data_ingestion_processing.feature_creation.reshape import SalesReshaper
from src_production_deployment.data_ingestion_processing.feature_creation.lag_feature import LagFeatureGenerator
from src_production_deployment.data_ingestion_processing.feature_creation.rolling_features import RollingFeatureGenerator
from src_production_deployment.data_ingestion_processing.feature_creation.sales_join import PriceJoiner
from src_production_deployment.data_ingestion_processing.feature_creation.price_features import PriceFeatureGenerator

from src_production_deployment.data_ingestion_processing.validation.test_loader import call_data_loader

data = call_data_loader(account_name="stdemandforecastingdev",filesystem="demand-forecasting")

reshape = SalesReshaper()
Calendar_Joiner = CalendarJoiner()
lag_generator = LagFeatureGenerator()
rolling_generator = RollingFeatureGenerator()
price_joiner = PriceJoiner()
price_feature = PriceFeatureGenerator()

sales_long = reshape.transform(data.sales)
#print(sales_long.head(10))

merged = Calendar_Joiner.transform(sales_long, data.calendar)
#print(merged.head(10))

lag_features = lag_generator.transform(merged)
#print(lag_features.head(10))

rolling_features = rolling_generator.transform(lag_features)
#print(rolling_features.head(10))

priced  = price_joiner.transform(rolling_features, data.prices)
#print(priced.head(10))

featured = price_feature.transform(priced)

print(
    featured[
        [
            "item_id",
            "store_id",
            "wm_yr_wk",
            "sell_price",
            "price_change",
            "price_pct_change",
            "discount_flag"
        ]
    ].head()
)

print(featured.shape)