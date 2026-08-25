from abc import ABC, abstractmethod


class BaseTuningStrategy(ABC):

    @abstractmethod
    def fit(self, X_train, y_train):
        pass

    @abstractmethod
    def get_best_params(self):
        pass

    @abstractmethod
    def get_best_score(self):
        pass

    @abstractmethod
    def get_best_estimator(self):
        pass

    @abstractmethod
    def get_cv_results(self):
        pass