import boto3

# Create s3 clinet

s3 = boto3.client("s3")

# List all s3 buckets

response = s3.list_buckets()

print('Connected to AWS')

print("Available buckets")
for bucket in response["Buckets"]:
    print(f" - {bucket['Name']}")