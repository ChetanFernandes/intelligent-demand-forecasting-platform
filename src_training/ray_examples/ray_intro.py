import ray
ray.init()
from ray import tune

def train_function(config):
    score = (config["x"] - 5) ** 2
    tune.report(rmse=score)

search_space = {"x": tune.uniform(0,10)}

tuner = tune.Tuner(train_function, param_space = search_space, tune_config = tune.TuneConfig(num_samples=20))

results = tuner.fit()

best_result = results.get_best_result(metric="rmse", mode="min")

print(best_result.config)

print(best_result.metrics["rmse"])




'''
@ray.remote
def main(x):
    return x * x

result1 = main.remote(5)
result2 = main.remote(10)
result3 = main.remote(20)

answers = ray.get([result1, result2, result3])

print(answers)
print(ray.available_resources())

if __name__=="main":
    main()

     param_space
      │
      ▼
Generate Configuration
      │
      ▼
config
      │
      ▼
trainable(config)
      │
      ▼
Train Model
      │
      ▼
tune.report()
'''