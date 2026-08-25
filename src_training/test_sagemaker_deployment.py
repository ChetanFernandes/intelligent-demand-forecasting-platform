import sys
sys.path.insert(0,r"D:\sagemaker_model_package")
import numpy as np

def prediction(test_input):
    import inference
    MODEL_DIR = r"D:\sagemaker_model_package"
    model = inference.model_fn(MODEL_DIR)


    print("Model loaded successfully")

    print("Model type:", type(model))


    columns = test_input.select_dtypes(include = "object").columns.to_list()
                   
    for col in columns:

        test_input[col] = test_input[col].astype("category")


    if "sales" in test_input.columns:
                
        test_input = test_input.drop(columns=["sales"])
    
 
    test_input = test_input.loc[~test_input["event_name_1"].isin(["OrthodoxEaster","Pesach End"])]

    test_input["event_name_1"] = (test_input["event_name_1"].cat.remove_unused_categories())

    predictions = inference.predict_fn(test_input, model)

    #predictions = np.asarray(predictions).ravel()

    test_input["sales"] = predictions
    
    print("Prediction:", predictions[:10])

    return test_input

  

