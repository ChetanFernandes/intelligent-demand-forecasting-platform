LIGHTGBM_OPTUNA_PARAMETER_SPACE = {

    "learning_rate": {
        "type": "float",
        "low": 0.01,
        "high": 0.10
    },

    "num_leaves": {
        "type": "int",
        "low": 20,
        "high": 50
    },

    "max_depth": {
        "type": "categorical",
        "choices": [-1, 4, 6, 8]
    },

    "min_child_samples": {
        "type": "int",
        "low": 10,
        "high": 40
    },

    "colsample_bytree": {
        "type": "float",
        "low": 0.7,
        "high": 1.0
    },

    "subsample": {
        "type": "float",
        "low": 0.7,
        "high": 1.0
    },

    "subsample_freq": {
        "type": "int",
        "low": 1,
        "high": 5
    },

    "min_split_gain": {
        "type": "float",
        "low": 0.0,
        "high": 1.0
    },

    "reg_alpha": {
        "type": "float",
        "low": 0.0,
        "high": 1.0
    },

    "reg_lambda": {
        "type": "float",
        "low": 0.0,
        "high": 2.0
    },

    "n_estimators": {
        "type": "int",
        "low": 100,
        "high": 300
    }
}


XGBOOST_OPTUNA_PARAMETER_SPACE = {

    "learning_rate": {
        "type": "float",
        "low": 0.03,
        "high": 0.10
    },

    "max_depth": {
        "type": "int",
        "low": 4,
        "high": 10
    },

    "min_child_weight": {
        "type": "int",
        "low": 5,
        "high": 15
    },

    "subsample": {
        "type": "float",
        "low": 0.6,
        "high": 1.0
    },

    "colsample_bytree": {
        "type": "float",
        "low": 0.6,
        "high": 1.0
    },

    "gamma": {
        "type": "float",
        "low": 0,
        "high": 5
    },

    "reg_alpha": {
        "type": "float",
        "low": 0,
        "high": 1
    },

    "reg_lambda": {
        "type": "float",
        "low": 0,
        "high": 5
    },

    "n_estimators": {
        "type": "int",
        "low": 100,
        "high": 300
    }
}

CATBOOST_OPTUNA_PARAMETER_SPACE = {

    "learning_rate": {
        "type": "float",
        "low": 0.03,
        "high": 0.10
    },

    "depth": {
        "type": "int",
        "low": 8,
        "high": 12
    },

    "iterations": {
        "type": "int",
        "low": 200,
        "high": 400
    },

    "l2_leaf_reg": {
        "type": "float",
        "low": 1.0,
        "high": 10.0
    },

    "random_strength": {
        "type": "float",
        "low": 0.0,
        "high": 5.0
    },

    "border_count": {
        "type": "categorical",
        "choices": [64, 128, 255]
    },

    "subsample": {
        "type": "float",
        "low": 0.6,
        "high": 1.0
    },

    "rsm": {
        "type": "float",
        "low": 0.6,
        "high": 1.0
    },

    "min_data_in_leaf": {
        "type": "int",
        "low": 5,
        "high": 30
    }
}