import optuna
from src_training.tuning.strategies.base_stratergy import BaseTuningStrategy
from src_training.tuning.strategies.optuna.objectives.objectives_factory import ObjectiveFactory
import pandas as pd
from src_training.tuning.visualization.optuna_visualizer import OptunaVisualizer
from pathlib import Path
from datetime import datetime

class OptunaTuner(BaseTuningStrategy):

    def __init__(self,estimator,parameter_space,algorithm, n_trials=30,scoring="rmse",n_splits=4,random_state=42):

        self.estimator = estimator
        self.parameter_space = parameter_space
        self.n_trials = n_trials
        self.scoring = scoring
        self.n_splits = n_splits
        self.random_state = random_state
        self.algorithm = algorithm

        # n_trails means 

    def fit(self, X_train, y_train):
        
        objective = ObjectiveFactory.create(algorithm=self.algorithm, estimator = self.estimator, parameter_space = self.parameter_space, X_train=X_train, y_train=y_train, n_splits=self.n_splits)
         
        database_path = (Path("artifacts") / "optuna" / "optuna.db").resolve()

        database_path.parent.mkdir(parents=True, exist_ok=True)

        storage = f"sqlite:///{database_path.as_posix()}" #Every trial get stored in database

        print(storage)

        self.study = optuna.create_study(direction="minimize", sampler=optuna.samplers.TPESampler(seed=self.random_state), 
                                         pruner=optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=2), storage=storage, 
                                         study_name= f"{self.algorithm.value}_{datetime.now():%Y%m%d_%H%M%S}", load_if_exists=True) # Tree-structured Parzen Estimator.
 
        #sampler=optuna.samplers.TPESampler(seed=self.random_state),
        #✅ Uses the TPE algorithm to choose the next hyperparameters.
        #✅ Learns from previous trials.
        #✅ Balances exploration (trying new regions) and exploitation (searching around good regions).
        #✅ seed=self.random_state makes the sequence of sampled hyperparameters reproducible.

        self.study.optimize(objective,n_trials=self.n_trials)

        '''
        Internally Optuna does something like:
        for i in range(3):
        trial = Trial()
        score = objective(trial)
        save(score)
        Notice something important. You never wrote: objective(trial) . Optuna calls it
        '''

        visualizer = OptunaVisualizer(study=self.study, algorithm=self.algorithm.value)

        visualizer.generate_all()

    def get_best_params(self):
        return self.study.best_params
    
    def get_best_score(self):
        return self.study.best_value
    
    def get_best_estimator(self):
        return None
    
    def get_cv_results(self):
        results = []
        print(len(self.study.trials))

        for trial in self.study.trials:
            
            print(trial.number, trial.state, trial.value)

            row = {
                "trial": trial.number,
                "rmse": trial.value,
                **trial.params
            }
            results.append(row)
            
        results_df = pd.DataFrame(results)

        print(results_df.columns)
        print(results_df.head())

        # Smaller RMSE is better
        results_df = results_df.sort_values(by="rmse").reset_index(drop=True)

        # Add Rank column
        results_df.insert(0, "Rank", results_df.index + 1)

        return results_df

'''
TuningPipeline
        │
        ▼
OptunaTuner.fit()
        │
        ▼
ObjectiveFactory
        │
        ▼
LightGBMObjective
        │
        ▼
Study.optimize()
        │
        ▼
──────── Trial 1 ────────
        │
        ▼
ParameterSpaceConverter
        │
        ▼
LightGBMTrainingEngine
        │
        ▼
RMSE
        │
        ▼
Optuna stores result
──────── Trial 2 ────────
        │
        ▼
ParameterSpaceConverter
        │
        ▼
LightGBMTrainingEngine
        │
        ▼
RMSE
        │
        ▼
Optuna stores result
──────── Trial N ────────
        │
        ▼
Best Params
Best Score
All Trials
'''

'''
Without storage - Imagine - study = optuna.create_study()

The study exists only in memory.

You run - 100 trials - Then your laptop crashes. - Everything is gone. - You must start again from Trial 1.

With SQLite - Suppose you completed

Trial 1

Trial 2

...

Trial 83

Then the machine crashes.

Later you rerun your program.

Because you wrote

load_if_exists=True

Optuna opens the existing database.

It sees

Study already exists.

Completed trials = 83

and continues with

Trial 84

instead of starting over.

Another advantage

After training you can inspect the study later.

For example

study.best_params
study.best_value
study.trials_dataframe()

All of this comes from the SQLite database.

Enterprise benefit

Imagine running

10,000 trials

which takes

2 days

You definitely don't want to lose that work because of:

Power failure
Laptop restart
Server reboot
Exception during training

Persistent storage protects your optimization history.

Complete flow
OptunaTuner.fit()
        │
        ▼
Create SQLite database
        │
        ▼
Create Study
        │
        ▼
Trial 1  ─────► Save to SQLite
        │
Trial 2  ─────► Save to SQLite
        │
Trial 3  ─────► Save to SQLite
        │
...
        │
Trial N  ─────► Save to SQLite
        │
        ▼
Best Trial
Is it necessary?
For learning or quick experiments: No. You can omit storage and keep everything in memory.
For production-quality ML frameworks: Yes, it's a very good practice. It makes experiments resumable, reproducible, and easier to analyze later.

For the MLOps framework you're building, storing studies in SQLite under artifacts/optuna is a solid design choice because it aligns with how long-running experiment tracking is typically handled in production systems.
'''