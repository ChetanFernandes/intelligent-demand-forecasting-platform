class ComparisonReport:
    
    @staticmethod
    def generate(comparision_df, champion):
        print("/n" + "=" * 70)
        print("Model comparision report".center(70))
        print("="*70)
        print(comparision_df[
        [
            "Rank",
            "model_name",
            "rmse",
            "mae",
            "mape",
            "wape",
            "smape",
            "rmsse",
            "training_time"
        ]
    ].to_string(index=False)
)
       
        
