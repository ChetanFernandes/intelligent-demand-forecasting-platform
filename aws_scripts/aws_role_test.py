import boto3

iam = boto3.client("iam")

role_name = "SageMakerExecutionRole"

response = iam.get_role(RoleName=role_name)

print("=" * 60)
print("Execution Role Found")
print("=" * 60)

print(f"Role Name : {response['Role']['RoleName']}")
print(f"Role ARN  : {response['Role']['Arn']}")