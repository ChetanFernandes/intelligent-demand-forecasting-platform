from ray import tune
from scipy.stats import randint, uniform
from sagemaker.tuner import (HyperparameterTuner, IntegerParameter, ContinuousParameter, CategoricalParameter,)

class ParameterSpaceConverter:

    @staticmethod
    def to_ray(parameter_space):
        ray_space = {}
        for name, config in parameter_space.items():
            if config['type'] == "float":
                ray_space[name] = tune.uniform(config["low"], config["high"])

            elif config['type'] == "int":
                ray_space[name] = tune.randint(config["low"], config["high"] + 1)

            
            elif config['type'] == "categorical":
                ray_space[name] = tune.choice(config["choices"])
        
        print(ray_space)
        return ray_space


    @staticmethod
    def to_optuna(parameter_space, trial):

        optuna_space = {}

        for name, config in parameter_space.items():
            
            if config['type'] == "float":
                optuna_space[name] = trial.suggest_float(name,config["low"], config["high"])

            elif config['type'] == "int":
                optuna_space[name] = trial.suggest_int(name,config["low"], config["high"])

            elif config['type'] == "categorical":
                optuna_space[name] = trial.suggest_categorical(name,config["choices"])
        
        print(optuna_space)
        
        return optuna_space


    @staticmethod
    def to_sagemaker(parameter_space):

        sm_space = {}

        for name, config in parameter_space.items():

            if config["type"] == "float":

                sm_space[name] = ContinuousParameter(
                    config["low"],
                    config["high"],
                )

            elif config["type"] == "int":

                sm_space[name] = IntegerParameter(
                    config["low"],
                    config["high"],
                )

            elif config["type"] == "categorical":

                sm_space[name] = CategoricalParameter(
                    config["choices"],
                )

        return sm_space