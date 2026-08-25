import pandas as pd

class BlendingSplitter:

    def split(self, X_val:pd.DataFrame, y_val:pd.DataFrame) -> pd.DataFrame:
        # X_val preserves the chronological order from DataSplitter,
        # so splitting by index is equivalent to splitting the
        # 28-day validation window into two sequential halves
         
        split_index = len(X_val) // 2
        print(split_index)

        X_blend_train = X_val.iloc[:split_index] 
        y_blend_train = y_val.iloc[:split_index]

        X_blend_validation = X_val.iloc[split_index:]
        y_blend_validation = y_val.iloc[split_index:]
        return (
            X_blend_train,
            X_blend_validation,
            y_blend_train,
            y_blend_validation,
        )





