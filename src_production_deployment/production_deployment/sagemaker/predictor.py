import boto3
import json

class SageMakerPredictor:
    def __init__(self,endpoint_name:str,region_name:str):
        self.endpoint_name = endpoint_name
        self.client = boto3.client("sagemaker-runtime",region_name = region_name) 
        # creates a client that can communicate with a deployed SageMaker endpoint.

    def predict(self,data):
        payload = data.to_json(orient = "records")
        response = self.client.invoke_endpoint(EndpointName=self.endpoint_name, ContentType="application/json", Body=payload)
        # "AWS, invoke this deployed SageMaker endpoint and give it this input."
        # response
        '''
        {
            "ContentType": "application/json",
            "Body": <streaming response body>
        }
        '''
        # Body is a stream. Read the actual bytes returned by SageMaker."
        # .decode("utf-8") - b'[0.4012232435664078]' - '[0.4012232435664078]'
        result = response["Body"].read().decode("utf-8")
        predictions = json.loads(result) # Convert JSON string back to Python - [0.4012232435664078]
        data = data.copy()
        data["sales"] = predictions
        return data



