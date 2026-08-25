import boto3
import requests
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

region = "us-east-1"
service = "monitoring"
url = "https://monitoring.us-east-1.amazonaws.com/api/v1/query"

params = {
    "query": "aws_sagemaker_invocations_sum"
}

session = boto3.Session(region_name=region)
credentials = session.get_credentials().get_frozen_credentials()

request = AWSRequest(
    method="GET",
    url=url,
    params=params,
)

SigV4Auth(credentials, service, region).add_auth(request)

prepared = request.prepare()

response = requests.get(
    prepared.url,
    headers=dict(prepared.headers),
)

print("STATUS:", response.status_code)
print("RESPONSE:")
print(response.text)