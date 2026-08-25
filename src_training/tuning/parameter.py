from scipy.stats import randint, uniform


CATBOOST_PARAMETER_RANDOM = {

    "learning_rate": uniform(0.03, 0.11),

    "depth": randint(10, 15),

    "min_data_in_leaf": randint(5,10),

    "iterations": randint(250, 350)
}


LIGHTGBM_PARAMETER_RANDOM = {

    "learning_rate": uniform(0.01, 0.09),

    "num_leaves": randint(20, 41),

    "max_depth": [-1, 4, 6, 8],

    "min_child_samples": randint(10, 31),

    "n_estimators": randint(100, 251)
}

LIGHTGBM_PARAMETER_GRID = {
    "learning_rate": [0.01, 0.03],
    "num_leaves": [20],
    "max_depth": [4],
    "min_child_samples": [10, 20],
    'n_estimators': [200]
}




''' 
Summary
Search Method	          List	                         uniform()	  randint()
GridSearchCV	           ✅	                           ❌	      ❌
RandomizedSearchCV	       ✅	                           ✅	      ✅
Optuna	                   ❌ (uses suggest_*)	           ✅	      ✅
SageMaker HPO	           ❌	                           ✅ (via ContinuousParameter)	✅ (via IntegerParameter)
Ray Tune	               ❌	                           ✅	      ✅

This is exactly why, in your framework, it makes sense to maintain:

PARAMETER_GRID → for Grid Search (lists only)
PARAMETER_DISTRIBUTIONS → for Random Search (lists and SciPy distributions)
PARAMETER_SPACE → for Optuna, Ray Tune, and SageMaker (ranges/distributions)

That separation aligns with how each tuning library is designed to work.
'''