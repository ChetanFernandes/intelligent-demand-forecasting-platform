from configs.project_config import HYPERPARAMETER_DIR
from src_training.tuning.hyperparameter_manager import HyperparameterManager
from src_training.tuning.stratergy_factory import TuningstratergyFactory


class TuningPipeline:
    """This pipeline writes the YAML."""

    def __init__(self, estimator, parameter_space, algorithm, stratergy, tuning_config = None):

        self.stratergy = stratergy

        self.algorithm = algorithm

        self.tuner = TuningstratergyFactory.create(stratergy = stratergy, estimator = estimator, parameter_space = parameter_space, algorithm=algorithm, 
                                                   tuning_config=tuning_config)

        
    def run(self, X_train, y_train, job_name ): # job_name

        self.tuner.fit(job_name, X_train,y_train)
        print("Training completed")
        best_params = None
        best_score = None
        return best_params , best_score 

        
        '''
        best_params = self.tuner.get_best_params()
        print("best_parsms",best_params)

        best_score = self.tuner.get_best_score()
        print("Best_score",best_score)
 
        best_estimator =  self.tuner.get_best_estimator() # If refit is false, it will not give best estimator
        print("Best_hyperparmeetrs",best_estimator.hyperparameters())
        print("Best_estimator", best_estimator.model_data) # best trained model

        results = self.tuner.get_cv_results()

        config_path = HYPERPARAMETER_DIR/self.algorithm.value/f"{self.stratergy.value}.yaml"

        HyperparameterManager.save(best_params, config_path)

        HyperparameterManager.save_csv_results(results = results, algorithm = self.algorithm.value, stratergy = self.stratergy.value)

        return ( best_params, best_score )
        '''
        


