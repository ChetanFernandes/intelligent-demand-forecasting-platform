import pandas as pd
import os
import cloudpickle
from flask import Flask, request, jsonify


app = Flask(__name__)

def model_fn(model_dir):
    model_path = os.path.join(model_dir,"model.pkl")
    with open(model_path,"rb") as f:
         model = cloudpickle.load(f)
    return model

MODEL_DIR = "/opt/ml/model"
model = model_fn(MODEL_DIR) # means the model is loaded once when the container starts

@app.route("/ping", methods = ["GET"])
def ping():
    return jsonify({"status":"healthy"})

@app.route("/invocations", methods = ["POST"])
def invocations():

    input_data = request.get_json()

    data = pd.DataFrame(input_data)

     # Convert object columns to categorical
    columns = data.select_dtypes(include="object").columns.to_list()
    for col in columns:
        data[col] = data[col].astype("category")
    
    # Remove target column if it is present
    if "sales" in data.columns:
        data = data.drop(columns=["sales"])

    # Remove unsupported event types
    data = data.loc[ ~data["event_name_1"].isin(["OrthodoxEaster", "Pesach End"])]

    # Remove unused event categories
    data["event_name_1"] = (data["event_name_1"].cat.remove_unused_categories())

    predictions = model.predict(data)
    
    return jsonify(predictions.tolist())

if __name__=="__main__":
    app.run(host = "0.0.0.0",port = 8080) # Flask listens incoming request on port 8080