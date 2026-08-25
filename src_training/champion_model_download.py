from src_training.registry.mlflow_registry import ModelRegistry
import mlflow
#from src.ensemble.data.blending_splitter import BlendingSplitter
#from src.evaluation.metrics_calculator import MetricsCalculator
import pandas as pd
import numpy as np
from logger.logging import setup_logging
log = setup_logging()

class champion_model_download:
    ''' Champion model download from mlflow to local'''
    def __init__(self,registry:ModelRegistry): #splitter:BlendingSplitter, evaluator:MetricsCalculator)
        self.registry = registry
        #self.splitter = splitter
        #self.evaluator = evaluator
        self.model_name = "DemandForecasting_Blending"
        self.version = "latest"


    def load_model_prediction(self, recursive_ready:pd.DataFrame) -> pd.DataFrame:

        model_uri = self.registry.get_model_uri(self.model_name, self.version)

        log.info("Model_uri %s",
                 model_uri)

        # model_details = self.registry.get_model_details( self.model_name,self.version)

        champion_model = mlflow.sklearn.load_model(model_uri)
        
        log.info("champion_model \n%s",
                 champion_model)

        #champion_model = mlflow.pyfunc.load_model(model_uri)

        #print("Type of champion model ",type(champion_model))
        #print("Ensemble_models",champion_model.ensemble_model.models)
        #print("Meta_model",champion_model.meta_model)
        #print("Type_of_meta_model",type(champion_model.meta_model))
        #for name, base_model in champion_model.ensemble_model.models.items():
            #print(name, type(base_model))
       
        #X_inference = pd.read_parquet(r"artifacts/recursive_prediction/recursive_ready.parquet")

        columns = recursive_ready.select_dtypes(include = "object").columns.to_list()
               
        for col in columns:

            recursive_ready[col] = recursive_ready[col].astype("category")

        

        if "sales" in recursive_ready.columns:
                    
            recursive_ready = recursive_ready.drop(columns=["sales"])
        
            log.info("Inference shape after removing target: \n%s", 
                     recursive_ready.shape)
 
        recursive_ready = recursive_ready.loc[~recursive_ready["event_name_1"].isin(["OrthodoxEaster","Pesach End"])]

        recursive_ready["event_name_1"] = (recursive_ready["event_name_1"].cat.remove_unused_categories())

        predictions = champion_model.predict(recursive_ready)

        predictions = np.asarray(predictions).ravel()

        log.info("Post_ravel \n%s ",
                 predictions)

        recursive_ready["sales"] = predictions

        return recursive_ready



        #metrics =  self.evaluator.calculate_metrics(Y_inference,predictions)
        #rmsse = calculate_rmsse(Y_train, y_true = Y_inference, y_pred = predictions)
        #print(metrics['rmse'])
        #print(rmsse)
      


if __name__ == "__main__":

    model_registry = ModelRegistry()
    #splitter = BlendingSplitter()
    #evaluator = MetricsCalculator()
    model_download = champion_model_download(model_registry)
    model_download.load_model()



       
'''
X_train = pd.read_parquet(r"artifacts/datasets/train_df.parquet")


categorical_columns = (X_train.select_dtypes(include="category").columns.to_list())

for col in categorical_columns:
    if col not in X_inference.columns:
        continue

    train_categories = X_train[col].cat.categories 
    # So .cat essentially tells pandas: "I want to work with the categorical metadata/operations of this Series."
    # And then .categories asks: "What is the category vocabulary?"

    X_inference[col] = (X_inference[col].astype("category").cat.set_categories(train_categories))


''' 

'''
predictions = champion_model.predict(X)

could potentially be:

numpy.ndarray
pandas.Series
pandas.DataFrame
list

.ravel() is a NumPy method, so:

predictions.ravel()

only works if the returned object supports it.

np.asarray() converts an array-like object into a NumPy array:

predictions = np.asarray(predictions).ravel()
'''

