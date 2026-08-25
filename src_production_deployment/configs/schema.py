
SALES_SCHEMA = { "required_columns" : ["id","item_id","dept_id","cat_id","store_id","state_id"],

                 "column_types" : {"id":"str","item_id":"str","dept_id":"str","cat_id":"str","store_id":"str","state_id":"str"},
                
                 "non_negative_prefixes":"d_"
            
                }

CALENDAR_SCHEMA = {

                  "required_columns" : [
                                           "date","wm_yr_wk","weekday","wday","month","year","d","event_name_1",
                                           "event_type_1","event_name_2","event_type_2","snap_CA","snap_TX","snap_WI"
                                        ],

                  "column_types": { "date": "object", "wm_yr_wk": "int64", "weekday": "object", "wday": "int64", "month": "int64",
                                    "year": "int64", "d": "object", "event_name_1": "object", "event_type_1": "object",
                                    "event_name_2": "object", "event_type_2": "object", "snap_CA": "int64",
                                    "snap_TX": "int64",
                                    "snap_WI": "int64"
                                 },

                   "non_nullable_columns": ["date", "wm_yr_wk", "weekday","wday","month","year","d","snap_CA","snap_TX","snap_WI"] 

                   }



SELL_PRICES_SCHEMA = { "required_columns" : ["store_id","item_id","wm_yr_wk","sell_price"],
                      
                       "column_types" : {"store_id": "str", "item_id":"str", "wm_yr_wk":"int64", "sell_price":"float64"},

                       "non_nullable_columns": ["store_id", "item_id", "wm_yr_wk", "sell_price"],

                       "non_negative_columns" : ["sell_price"] ,


                     }



EXPECTED_MISSING_COLUMNS  = ["event_name_1","event_type_1","event_name_2","event_type_2"]


