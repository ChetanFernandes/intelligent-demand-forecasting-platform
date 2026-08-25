from src_production_deployment.data_ingestion_processing.feature_creation.calendar_join import CalendarJoiner
#from src.data_ingestion_processing.feature_creation.reshape import SalesReshaper
from src_production_deployment.data_ingestion_processing.feature_creation.lag_feature import LagFeatureGenerator
from src_production_deployment.data_ingestion_processing.feature_creation.rolling_features import RollingFeatureGenerator
from src_production_deployment.data_ingestion_processing.feature_creation.price_features import PriceFeatureGenerator
#from src.data_ingestion_processing.ingestion.data_loader import call_data_loader
import pandas as pd
from src_production_deployment.data_ingestion_processing.validation.schema_validator import SchemaValidator
from src_production_deployment.data_ingestion_processing.validation.missing_values_validator import MissingValueValidator
from src_production_deployment.data_ingestion_processing.validation.outlier_validator import OutlierValidator
from src_production_deployment.data_ingestion_processing.validation.great_exception_validation import GXValidator
from src_production_deployment.data_ingestion_processing.preprocessing.missing_values_treatment import FillMissingValue
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()
import io


class DataLoader:

    def __init__(self, account_name = None, filesystem = None):

        self.account_name = account_name

        self.filesystem = filesystem

        #self.data = call_data_loader(account_name = "stdemandforecastingdev", filesystem = "demand-forecasting")

        self.schema_validator = SchemaValidator()
        self.missing_value = MissingValueValidator()
        self.outlier_validator = OutlierValidator()
        self.GX_validator = GXValidator()

    

    def convert_to_parquet_bytes(self,data:pd.DataFrame|bytes) -> io.BytesIO:

        if isinstance(data,bytes):
            data = pd.read_csv(io.BytesIO(data))
            log.info("Give data is in Bytes")
        else:
            log.info("Give data is a DataFrame")
            pass

        parquet_buffer = io.BytesIO()

        data.to_parquet(parquet_buffer,engine="pyarrow",index = False)

        parquet_buffer.seek(0)

        return parquet_buffer

    '''
    def load_to_s3_calendar(self, file_name:str):
        session = AWSSession()
        s3_manager = S3Manager(session)
        parquet_buffer = self.convert_to_parquet_bytes(self.data.calendar)
        s3_manager.upload_file_memory(parquet_buffer, key=f"forecast_data/{file_name}.parquet")

    

    def load_to_s3_sell_price(self,file_name:str):
        session = AWSSession()
        s3_manager = S3Manager(session)
        parquet_buffer = self.convert_to_parquet_bytes(self.data.prices)
        s3_manager.upload_file_memory(parquet_buffer, key=f"forecast_data/{file_name}.parquet")
    

    def load_to_s3(self, data, file_name:str):
        session = AWSSession()
        s3_manager = S3Manager(session)
        parquet_buffer = self.convert_to_parquet_bytes(data)
        s3_manager.upload_file_memory(parquet_buffer, key=f"forecast_data/{file_name}.parquet")
    


    def load_champion_model_s3(self,local_path:str):
        session = AWSSession()
        s3_manager = S3Manager(session)
        s3_manager.upload_champion_model_s3(local_path,"champion_model")
    '''


    def data_validation(self,report, calendar, sell_price, path):

        '''
        log.info(f"Validating_sales_data_set")
        self.schema_validator.sales_train_validate(self.data.sales,report)
        self.missing_value.validate(self.data.sales,"sales",report)
        self.outlier_validator.validate(self.data.sales,"sales",report,path)
        self.GX_validator.validate(self.data.sales,"sales",report)
        log.info(f"Validating_sales_data_set_completed")
        '''

        log.info(f"Validating_calendar_data_set")


        self.schema_validator.calendar_validation(calendar,report)
        self.missing_value.validate(calendar,"calendar",report)
        self.outlier_validator.validate(calendar,"calendar",report,path)
        self.GX_validator.validate(calendar,"calendar",report)

        log.info(f"Validating_calendar_data_set_completed")




        log.info(f"Validating selling price dataset")

        self.schema_validator.sell_price_validator(sell_price,report)
        self.missing_value.validate(sell_price,"price",report)
        self.outlier_validator.validate(sell_price,"price",report,path)
        self.GX_validator.validate(sell_price,"price",report)

        log.info(f"Validating selling price dataset completed")

    def data_re_validation(self,report, calendar):

     
        #log.info(f"Validating_sales_data_set")
        #self.schema_validator.sales_train_validate(self.data.sales,report)
        #self.missing_value.validate(self.data.sales,"sales",report)
        #self.outlier_validator.validate(self.data.sales,"sales",report,)
        #self.GX_validator.validate(self.data.sales,"sales",report)
        #log.info(f"Validating_sales_data_set_completed")
     

        log.info(f"Validating_calendar_data_set")

        #self.schema_validator.calendar_validation(self.data.calendar,report)
        self.missing_value.validate(calendar,"calendar",report)
        #self.outlier_validator.validate(self.data.calendar,"calendar",report)
        #self.GX_validator.validate(self.data.calendar,"calendar",report)

        log.info(f"Validating_calendar_data_set_completed")

        #log.info(f"Validating selling price dataset")
        #self.schema_validator.sell_price_validator(self.data.prices,report)
        #self.missing_value.validate(self.data.prices,"price",report)
        #self.outlier_validator.validate(self.data.prices,"price",report)
        #self.GX_validator.validate(self.data.prices,"price",report)
        #log.info(f"Validating selling price dataset completed")


    def data_preprocessing(self,calendar):

        fill_values = FillMissingValue()

        fill_values.values(calendar)

    '''
    def data_massaging(self,path):
        'Reshaping , adding extra columns and combining sales, price and calendar data'

        reshape = SalesReshaper()
      
        sales_reshaped, future_rows_unique  = reshape.transform(self.data.sales)

        log.info("sales_evaluation_reshaped - shape %s " , sales_reshaped.shape)
        log.info("future_rows_unique - shape -  %s " , future_rows_unique.shape)

        log.info("Loading s3_reshaped and future rows to S3")

        self.load_to_s3(sales_reshaped, "sales_reshaped")
        self.load_to_s3(future_rows_unique, "future_rows_unique")
        
        log.info("Loading completed")

        future_rows_unique.to_csv(path/"future_rows_unique.csv")
        future_rows_unique.to_parquet(path/"future_rows_unique.parquet")

        sales_reshaped.to_csv(path/"sales_reshaped.csv")
        sales_reshaped.to_parquet(path/"sales_reshaped.parquet")

        del self.data.sales
        del sales_reshaped
        del future_rows_unique
     
        gc.collect()
    '''
    
    


    def calendar_joiner(self, combined, calendar):

        joiner = CalendarJoiner()

        combined_calendar_merged = joiner.transform(combined, calendar)

        return combined_calendar_merged
        

   
    def feature_generation_recursive(self,combined:pd.DataFrame,sell_price) -> pd.DataFrame:

        lag_generator = LagFeatureGenerator()
        rolling_generator = RollingFeatureGenerator()
        price_feature = PriceFeatureGenerator()

        lag_features = lag_generator.transform(combined)

        rolling_features = rolling_generator.transform(lag_features)

        del lag_features

        price_joined = rolling_features.merge(sell_price, on=["item_id", "store_id", "wm_yr_wk"], how="left")
        
        price_transformation = price_feature.transform(price_joined)

        log.info(price_transformation.loc[price_transformation["day"] == "d_1943" , ["lag_1","lag_7","lag_28","rolling_mean_7","rolling_mean_28","sell_price","price_change","price_pct_change"]].isna().sum())

        del price_joined

        return price_transformation


    def  drop_columns_recursive(self,df:pd.DataFrame,day:str,path:str) -> pd.DataFrame:
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

        recursive_ready.to_csv(path/f"recursive_ready_{day}.csv",index = False)
        
        recursive_ready.to_parquet(path/f"recursive_ready_{day}.parquet",index = False)

        return recursive_ready


    
    








