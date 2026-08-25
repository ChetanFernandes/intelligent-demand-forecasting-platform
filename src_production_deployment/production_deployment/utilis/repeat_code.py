import pandas as pd
from src_production_deployment.logger.logging import setup_logging

log = setup_logging()


def recurrsive_tasks(sales_reshaped,future_rows_unique, prediction_day, path, loader, calendar, sell_price, predictor, combined = None): 

        if combined is None:

            combined = pd.concat([sales_reshaped,future_rows_unique], ignore_index = True)

            log.info("combined shape for first iteration %s",combined.shape)

            combined = loader.calendar_joiner(combined, calendar)
       
        else:
            
            future_rows_unique = loader.calendar_joiner(future_rows_unique,calendar)
            
            combined = pd.concat([combined,future_rows_unique], ignore_index=True)

        combined["date"] = pd.to_datetime(combined["date"], dayfirst=True, errors="coerce")

        combined = combined.sort_values(["id","day"],kind="mergesort").reset_index(drop = True)

        combined.to_csv(path/f"combined_{prediction_day}.csv", index = False)

        combined.to_parquet(path/f"combined_{prediction_day}.parquet", index = False)

        log.info("combined shape after calendar merge %s",combined.shape)

        price_transformation = loader.feature_generation_recursive(combined,sell_price)

        log.info("price merged successfully")

        price_transformation.to_csv(path/f"price_transformation_{prediction_day}.csv", index = False)

        log.info("shape post price merged \n%s",
                  price_transformation.shape)
    
        recursive_ready = loader.drop_columns_recursive(price_transformation, prediction_day,path)

        #recursive_result = prediction(recursive_ready)
        
        recursive_result = predictor.predict(recursive_ready)

        recursive_result.to_csv(path/f"recursive_result_{prediction_day}.csv", index = False)

        recursive_result.to_parquet(path/f"recursive_result_{prediction_day}.parquet", index = False)

        return recursive_result , combined

def post_prediction_single_day(recursive_result,combined,future_rows,prediction_day):

        recursive_result = recursive_result[["sales"]] 
        
        future_ids = future_rows[["id"]]

        assert len(future_ids) == len(recursive_result)

        prediction_with_sales_id = pd.DataFrame({"id": future_ids["id"].to_numpy(),"sales":recursive_result["sales"].to_numpy()})

        prediction_map = prediction_with_sales_id.set_index("id")["sales"] # set index for column sales

        log.info("prediction_map \n%s", \
                  prediction_map[:10])

        log.info("prediction_map.shape %s", prediction_map.shape)

        mask = combined["day"] == prediction_day

        ids = combined.loc[mask,"id"] # These are the IDs for the d_1942 rows.

        combined.loc[mask,"sales"] = ids.map(prediction_map) # takes ids and and looks them up in prediction_map #df.loc[rows, columns]
        # combined.loc[mask, "sales"] - Give me the sales column only for the rows where mask is True.
        # combined.loc[mask, "sales"] = predictions For only the d_1942 rows, replace the existing sales values with the model's predictions.
        log.info("combined post attaching sales  \n%s", 
                 combined.loc[combined["day"] == prediction_day, ["id", "day", "sales"]].head(10))
        
        log.info("combined_shape_post_mapping_sales \n%s", 
                  combined.loc[combined["day"] == prediction_day].shape)
        
        log.info("count of sales columns being none\n%s",
                 combined.loc[combined["day"] == prediction_day, 'sales'].isna().sum())

        return combined