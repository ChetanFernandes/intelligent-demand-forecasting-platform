from pathlib import Path
import gc
from src_production_deployment.logger.logging import setup_logging
log = setup_logging()

class feature_selection:

    def feature(self,train_df, test_df,validation_df):

        try:

            # Seggregatig features and target values

            Y_train = train_df[["sales"]]

            X_train = train_df.drop(columns=["sales"])

            Y_test = test_df[["sales"]]

            X_test = test_df.drop(columns=["sales"])

            Y_val =  validation_df[["sales"]]

            X_val =  validation_df.drop(columns = ["sales"])

            del train_df, test_df, validation_df
                                    
            gc.collect()
            
        
            # Drop unwanted columns

            log.info(f"Train_data_shape_before_dropping_columns,{X_train.shape}")

            log.info(f"Test_data_shape_before_dropping_columns,{X_test.shape}")
            
            log.info(f"Validation_data_shape_defore_dropping_columns,{X_val.shape}")


      
            log.info(f"Total Columns before_dropping_columns: {len(X_train.columns)}")

            log.info(f"Total Columns before_dropping_columns: {len(X_test.columns)}")

            log.info(f"Total Columns before_dropping_columns: {len(X_val.columns)}")


            drop_columns = [
                "id",  # Redundant . Very high cardinality
                "date", # dropping becaus of raw date. We have wday , month and year
                "day",  # both day and d represent number of days
                "d",    # both day and d represent number of days d_1,d_2 - no business meaning drop
                "weekday", 
                # Looking at the M5 calendar: weekday = actual day name. wday = encoded day number from Walmart calendar.
                # Both contain the same information. Sunday -> 2. We don't need both. 
                # For ML: wday is easier because it's already numeric.
                
                "event_name_2", # dropping becuase of null values
                "event_type_2"  # dropping becuase of null values
                           ]


            X_train = X_train.drop(columns=drop_columns)

            X_test = X_test.drop(columns=drop_columns)

            X_val = X_val.drop(columns=drop_columns)


            log.info(f"Total Columns after dropping columns: {len(X_train.columns)}")

            log.info(f"Total Columns after dropping columns: {len(X_test.columns)}")
                    
            log.info(f"Total Columns after dropping columns: {len(X_val.columns)}")


            log.info(f"Train_data_shape_post_dropping_columns, {X_train.shape, Y_train.shape}")

            log.info(f"Test_data_shape_post_dropping_columns, {X_test.shape,Y_test.shape}")

            log.info(f"Validation_data_shape_post_dropping_columns,{X_val.shape,Y_val.shape}")

            path = Path("artifacts/datasets/data_split")

            path.mkdir(parents=True, exist_ok=True)
    
            Y_train.to_parquet(path/"Y_train.parquet")

            X_train.to_parquet(path/"X_train.parquet")

            Y_test.to_parquet(path/"Y_test.parquet")

            X_test.to_parquet(path/"X_test.parquet")

            Y_val.to_parquet(path/"Y_val.parquet")

            X_val.to_parquet(path/"X_val.parquet")
            

            Y_train.to_csv(path/"Y_train.csv")

            X_train.to_csv(path/"X_train.csv")

            Y_test.to_csv(path/"Y_test.csv")

            X_test.to_csv(path/"X_test.csv")

            Y_val.to_csv(path/"Y_val.csv")

            X_val.to_csv(path/"X_val.csv")

        except Exception:
            log.exception("Error occured during feature selection")
            raise

        
        '''
        print(X_train.dtypes) # To find the categorical columns
        categorical_columns = [
            "item_id",
            "dept_id",
            "cat_id",
            "store_id",
            "state_id",
            "event_name_1",
            "event_type_1",
        ]

        # To find the unique values in each columns (cardinalty) to check what encoding to be used
        for col in categorical_columns:
            print(f"{col}: {X_train[col].nunique()}")
        '''




