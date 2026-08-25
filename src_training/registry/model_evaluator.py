class ModelEvaluator:
    def __init__(self,metric_name = 'rmse'):
        self.metric_name = metric_name
    
    def is_better(self, current_rmse:float, current_rmsse:float, best_rmse:float, best_rmsse:float)-> bool:
        if current_rmse < best_rmse:
            return True
        
        if current_rmse == best_rmse and current_rmsse < best_rmsse:
            return True
        
        return False