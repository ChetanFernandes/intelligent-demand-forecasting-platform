import mlflow.pyfunc
from src_training.ensemble.models.ensemble_model import EnsembleModel
from src_training.ensemble.constant.constants import ENSEMBLE_MODELS, MODEL_VERSIONS
from src_training.registry.mlflow_registry import ModelRegistry

class ModelLoader:
    ''' Loading models from MLFLOW'''
    def __init__(self):
        mlflow.set_tracking_uri("sqlite:///mlflow.db")
        self.model_registry = ModelRegistry()

    def load(self) -> EnsembleModel:
        models = {}
        ''' 
        for model_name in ENSEMBLE_MODELS:
            model_uri = f"models:/{model_name}/latest"
            print(model_uri)
            models[model_name] = mlflow.pyfunc.load_model(model_uri)
        return EnsembleModel(models = models) #this return class instance or object
        '''

        for model_name in ENSEMBLE_MODELS:
            version = MODEL_VERSIONS[model_name]
            model_uri = self.model_registry.get_model_uri(model_name, version)
            model_details = self.model_registry.get_model_details(model_name,version)
            print(model_uri)
            print(model_details)
            models[model_name] = mlflow.pyfunc.load_model(model_uri)
        return EnsembleModel(models = models)

    '''
    def predict(self,ensemble_model):
        for model_name, model in ensemble_model.models.items():
            X_val = pd.read_parquet(r"artifacts/datasets/data_split/X_val.parquet")
            X_val = X_val[:5]
            print(X_val.shape)
            prediction = model.predict(X_val)
            print(model_name)
            print(prediction)



    if __name__=="__main__":
        loader = ModelLoader()
        ensemble_model  = loader.load() 
        print("Loaded Models:")
        #loader.predict(ensemble_model)
        #for name in ensemble_model.models:
            #print(f"✓ {name}")
    '''
    