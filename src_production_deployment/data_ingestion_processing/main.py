from src_production_deployment.data_ingestion_processing.feature_creation.calendar_join import CalendarJoiner
from src_production_deployment.data_ingestion_processing.feature_creation.reshape import SalesReshaper
from src_production_deployment.data_ingestion_processing.feature_creation.lag_feature import LagFeatureGenerator
from src_production_deployment.data_ingestion_processing.feature_creation.rolling_features import RollingFeatureGenerator
from src_production_deployment.data_ingestion_processing.feature_creation.sales_join import PriceJoiner
from src_production_deployment.data_ingestion_processing.feature_creation.price_features import PriceFeatureGenerator
from src_training.training.time_split import TimeSeriesSplitter
from pathlib import Path
from src_production_deployment.data_ingestion_processing.ingestion.data_loader import call_data_loader
from src_production_deployment.data_ingestion_processing.data_split_training import feature_selection
import pandas as pd
import gc
from src_production_deployment.data_ingestion_processing.validation.schema_validator import SchemaValidator
from src_production_deployment.data_ingestion_processing.validation.missing_values_validator import MissingValueValidator
from src_production_deployment.data_ingestion_processing.validation.outlier_validator import OutlierValidator
from src_production_deployment.data_ingestion_processing.validation.great_exception_validation import GXValidator
from src_production_deployment.data_ingestion_processing.preprocessing.missing_values_treatment import FillMissingValue
from abc import abstractmethod

from src_production_deployment.logger.logging import setup_logging
log = setup_logging()

class DataLoader:

    def __init__(self, account_name = None, filesystem = None):

        self.account_name = account_name

        self.filesystem = filesystem

        self.data = call_data_loader(account_name = account_name, filesystem = filesystem)

        self.schema_validator = SchemaValidator()
        self.missing_value = MissingValueValidator()
        self.outlier_validator = OutlierValidator()
        self.GX_validator = GXValidator()

    def data_validation(self,report):

        log.info(f"Validating_sales_data_set")

        self.schema_validator.sales_train_validate(self.data.sales,report)
        self.missing_value.validate(self.data.sales,"sales",report)
        self.outlier_validator.validate(self.data.sales,"sales",report)
        self.GX_validator.validate(self.data.sales,"sales",report)

        log.info(f"Validating_sales_data_set_completed")


        log.info(f"Validating_calendar_data_set")

        self.schema_validator.calendar_validation(self.data.calendar,report)
        self.missing_value.validate(self.data.calendar,"calendar",report)
        self.outlier_validator.validate(self.data.calendar,"calendar",report)
        self.GX_validator.validate(self.data.calendar,"calendar",report)

        log.info(f"Validating_calendar_data_set_completed")

        log.info(f"Validating selling price dataset")

        self.schema_validator.sell_price_validator(self.data.prices,report)
        self.missing_value.validate(self.data.prices,"price",report)
        self.outlier_validator.validate(self.data.prices,"price",report)
        self.GX_validator.validate(self.data.prices,"price",report)

        log.info(f"Validating selling price dataset completed")

    def data_re_validation(self,report):
    
        log.info(f"Validating_sales_data_set")

        self.schema_validator.sales_train_validate(self.data.sales,report)
        self.missing_value.validate(self.data.sales,"sales",report)
        self.outlier_validator.validate(self.data.sales,"sales",report)
        self.GX_validator.validate(self.data.sales,"sales",report)

        log.info(f"Validating_sales_data_set_completed")


        log.info(f"Validating_calendar_data_set")

        self.schema_validator.calendar_validation(self.data.calendar,report)
        self.missing_value.validate(self.data.calendar,"calendar",report)
        self.outlier_validator.validate(self.data.calendar,"calendar",report)
        self.GX_validator.validate(self.data.calendar,"calendar",report)

        log.info(f"Validating_calendar_data_set_completed")

        log.info(f"Validating selling price dataset")

        self.schema_validator.sell_price_validator(self.data.prices,report)
        self.missing_value.validate(self.data.prices,"price",report)
        self.outlier_validator.validate(self.data.prices,"price",report)
        self.GX_validator.validate(self.data.prices,"price",report)

        log.info(f"Validating selling price dataset completed")


    def data_preprocessing(self):

        fill_values = FillMissingValue()

        fill_values.values(self.data.calendar)


    def data_massaging(self,path):

        '''Reshaping , adding extra columns and combining sales, price and calendar data'''

        reshape = SalesReshaper()
      
        sales_reshaped, future_rows_unique  = reshape.transform(self.data.sales)

        log.info("sales_evaluation_reshaped %s " , sales_reshaped.shape)
        log.info("future_rows_unique %s " , future_rows_unique.shape)

        future_rows_unique.to_csv(path/"future_rows_unique.csv")
        future_rows_unique.to_parquet(path/"future_rows_unique.parquet")

        del self.data.sales
        
        log.info("sales_reshaped \n%s",
                 sales_reshaped.shape)

        sales_reshaped.to_csv(path/"sales_reshaped.csv")

        sales_reshaped.to_parquet(path/"sales_reshaped.parquet")
        
        del sales_reshaped
        del future_rows_unique
     

        gc.collect()

    def calendar_joiner(self, combined):
        joiner = CalendarJoiner()
        combined_calendar_merged = joiner.transform(combined, self.data.calendar)
        return combined_calendar_merged
        

    def feature_generation_recursive(self,combined:pd.DataFrame) -> pd.DataFrame:

        lag_generator = LagFeatureGenerator()
        rolling_generator = RollingFeatureGenerator()
        price_feature = PriceFeatureGenerator()

        lag_features = lag_generator.transform(combined)

        rolling_features = rolling_generator.transform(lag_features)

        del lag_features

        price_joined = rolling_features.merge(self.data.prices, on=["item_id", "store_id", "wm_yr_wk"], how="left")
        
        price_transformation = price_feature.transform(price_joined)

        log.info(price_transformation.loc[price_transformation["day"] == "d_1943" , ["lag_1","lag_7","lag_28","rolling_mean_7","rolling_mean_28","sell_price","price_change","price_pct_change"]].isna().sum())

        del price_joined

        return price_transformation

    def feature_generation(self, combined:pd.DataFrame):

        lag_generator = LagFeatureGenerator()
        rolling_generator = RollingFeatureGenerator()
        price_joiner = PriceJoiner()
        price_feature = PriceFeatureGenerator()

        lag_features = lag_generator.transform(combined)

        del combined

        rolling_features = rolling_generator.transform(lag_features)

        del lag_features

        price_joined = rolling_features.merge(self.data.price, on=["item_id", "store_id", "wm_yr_wk"], how="left")

        # merged , selling_price_missing , sales_column_with_missing_price  = price_joiner.transform(rolling_features, self.data.prices)
        #print("Price_joner", merged.dtypes.value_counts())

        path = Path("artifacts/production/missing_data/")

        path.mkdir(parents = True, exist_ok=True)

        file_name = (
                     f"selling_price_missing_report.csv"
                     #f"{datetime.now():%Y%m%d_%H%M%S}.csv"
                     )

        filepath = path/file_name

        selling_price_missing.to_csv(filepath, index = False)
        
        file_name = (
                     f"sales_column_with_missing_price.csv"
                     #f"{datetime.now():%Y%m%d_%H%M%S}.csv"
                     )

        filepath = path/file_name

        # Sales values for rows where selling price was missing
        sales_column_with_missing_price.to_frame(name="sales").to_csv(
            path / "sales_column_with_missing_price.csv",
            index=False
        )

        #priced.to_parquet("artifacts/datasets/sales_price.parquet")

        del selling_price_missing

        del sales_column_with_missing_price

        del rolling_features

        del self.data.prices

        gc.collect()

        featured = price_feature.transform(merged)

        print("featured",featured.dtypes.value_counts())

        #featured.to_parquet("artifacts/datasets/sales_features.parquet")

        featured.to_csv("artifacts/production/features_final.csv", index = False)

        del merged

        gc.collect()

        return featured
       

 
    def split_data(self, featured):

        ''' Splitting time series data into train, test and validation '''

        splitter = TimeSeriesSplitter()

        train_df, test_df, validation_df = splitter.split(featured)

        train_df = train_df.reset_index(drop=True)

        test_df = test_df.reset_index(drop=True)

        validation_df = validation_df.reset_index(drop=True)

        del featured

        gc.collect()

        log.info(f"\nTrain")
        
        log.info(f"{train_df["date"].min(), "->", train_df["date"].max()}")

        log.info(f"\nValidation")

        log.info(f"{validation_df["date"].min(), "->", validation_df["date"].max()}")

        log.info("\nTest")
        
        log.info(f"{test_df["date"].min(), "->", test_df["date"].max()}")

        train_df.to_parquet("artifacts/datasets/train_df.parquet")

        train_df.to_csv("artifacts/datasets/train_df.csv")

        test_df.to_parquet("artifacts/datasets/test_df.parquet")

        test_df.to_csv("artifacts/datasets/test_df.csv")

        validation_df.to_parquet("artifacts/datasets/validation_df.parquet")

        validation_df.to_csv("artifacts/datasets/validation_df.csv")

    
    def seg_x_y_drop_columns(self):

        train_df = pd.read_parquet("artifacts/datasets/train_df.parquet")

        test_df = pd.read_parquet("artifacts/datasets/test_df.parquet")

        validation_df = pd.read_parquet("artifacts/datasets/validation_df.parquet")

        feature_select = feature_selection()

        feature_select.feature(train_df, test_df, validation_df)


    def prepare_inference_features(self,df:pd.DataFrame) -> pd.DataFrame:
        """ This is applicable only for production infrence"""
     
        log.info(f"Shape before dropping null rows {df.shape}")

        # Keep these logs BEFORE dropping day/date
        log.info("Min day before dropping null rows: %s", df["day"].min())

        required_features = [
            "lag_28",
            "rolling_mean_28",
            "rolling_std_7"
        ]

        log.info("Dropping rows having null values from columns: %s", required_features)

        # Capture rows that will be dropped

        df_dropped = df[df[required_features].isna().any(axis=1)].copy()

        # Remove rows without required historical features

        df = df.dropna(subset=required_features)
 
       
        # Save dropped rows for investigation/audit
        missing_data_path = Path("artifacts/production/missing_data")

        missing_data_path.mkdir(parents=True, exist_ok=True)

        df_dropped.to_csv(missing_data_path / "df_dropped.csv", index=False)


        log.info("Shape after dropping null rows: %s", df.shape)

        log.info("Min day after dropping null rows: %s", df["day"].min())
      
       
        # Drop columns not required by the production model
        drop_columns = [
                        "id",
                        "date",
                        "day",
                        "d",
                        "weekday",
                        "event_name_2", 
                        "event_type_2"  
                    ]

        df = df.drop(columns = drop_columns)

        df = df.reset_index(drop=True)

        log.info("Shape after dropping unwanted columns: %s", df.shape)

        df.to_csv("artifacts/production/inference_ready.csv",index = False)

        return df


    def  drop_columns_recursive(self,df:pd.DataFrame,day:str) -> pd.DataFrame:
            """ This is applicable only for production infrence"""
         
            log.info("shape before taking out past days and keeping only prediction day %s",
                                 df.shape)

    
            prediction_df = df[df["day"] == day].copy()

            log.info("shape after keeping only prediction day %s",
                        prediction_df.shape)

            log.info(
                    "Prediction day %s null counts:\n%s",
                    day,
                    prediction_df.isna().sum()
                )

    
            required_features = [
                "lag_28",
                "rolling_mean_28",
                "rolling_std_7"
            ]
    
            assert not prediction_df[required_features].isna().any().any()
    

            # Drop columns not required by the production model
            drop_columns = [
                            "id",
                            "date",
                            "day",
                            "d",
                            "weekday",
                            "event_name_2", 
                            "event_type_2"
                        ]
    
            recursive_ready = prediction_df.drop(columns = drop_columns)
    
            recursive_ready = recursive_ready.reset_index(drop=True)
    
            log.info("Shape after dropping unwanted columns: %s", recursive_ready.shape)
    
            recursive_ready.to_csv(f"artifacts/recursive_prediction/recursive_ready_{day}.csv",index = False)
            recursive_ready.to_parquet(f"artifacts/recursive_prediction/recursive_ready_{day}.parquet",index = False)
    
            return recursive_ready
    








