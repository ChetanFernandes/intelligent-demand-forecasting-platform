aws sts get-caller-identity
aws configure get region
aws ecr describe-images --repository-name demand-forecasting --region us-east-1 --query "imageDetails[*].{Tags:imageTags,Digest:imageDigest,PushedAt:imagePushedAt}" --output table  >> to check whats inside repor
 

>> Milestone - 1 - Steps to push docker image to ECR (AWS)

    Step - 1 — Authenticate Docker with ECR - Docker needs permission to push an image into ECR.
        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 135053048192.dkr.ecr.us-east-1.amazonaws.com   

    Step - 2 — Tag your existing API image - It simply gives the same image another name/tag.
        docker tag api_image:latest 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting (ECR URI)

    step - 3 - Docker Push
        docker push 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:api-v1

>> Milestone - 2 - To prepare the EC2 production machine.

    step - 5 - check your existing EC2 instances
        aws ec2 describe-instances --region us-east-1 --query "Reservations[].Instances[].[InstanceId,State.Name,InstanceType,PublicIpAddress,PrivateIpAddress,Tags[?Key=='Name'].Value|[0]]" --output table

    step -6 - check your available VPC
        aws ec2 describe-vpcs --region us-east-1 --query "Vpcs[].[VpcId,CidrBlock,IsDefault]" --output table

    step - 7 - find the default subnet
        aws ec2 describe-subnets --region us-east-1 --filters "Name=vpc-id,Values=vpc-0a0f89f8075ff0c57" --query "Subnets[].[SubnetId,AvailabilityZone,CidrBlock,MapPublicIpOnLaunch]" --output table

    step - 8 - check whether you already have an EC2 security group
        aws ec2 describe-instances --instance-ids i-04d5a03f6be8c9ad4  --query "Reservations[].Instances[].SecurityGroups[]" --output table

    step - 9 - Create a security group
        aws ec2 create-security-group --group-name demand-forecasting-prod-sg --description "Security group for Intelligent Demand Forecasting production" --vpc-id vpc-0a0f89f8075ff0c57 --region us-east-1

        output  >>

                {
                "GroupId": "sg-0fd7498accef2485c",
                "SecurityGroupArn": "arn:aws:ec2:us-east-1:135053048192:security-group/sg-0fd7498accef2485c"
                }

    Step - 10 - Configure inbound access 

    step - 11 -  Determine your current public IP address, because SSH (port 22) should ideally be restricted 
                 to your IP rather than openedto the whole internet.

        curl https://checkip.amazonaws.com

        Output >> 49.206.133.86

    step - 12 - Add SSH rules first
        aws ec2 authorize-security-group-ingress --group-id sg-0fd7498accef2485c --protocol tcp --port 22 --cidr 49.206.133.86/32 --region us-east-1
        This creates (Now from my laptop public ip (49.206.133.86/32) i can connect to EC2 instance which we wil be creating)
        Port       : 22
        Protocol   : TCP
        Source     : 49.206.133.86/32
        Purpose    : SSH access from your computer

    step - 13 - After above command succeeds run below command
       aws ec2 describe-security-groups --group-ids sg-0fd7498accef2485c --region us-east-1 --query "SecurityGroups[0].IpPermissions" --output table

    step - 14 - Before creating the EC2, we need to decide which AMI (Linux operating system image) to use. For our Docker-based deployment, we'll most likely use Amazon Linux 2023.  Let's find the current Amazon Linux 2023 AMI in us-east-1.

        aws ec2 describe-images --region us-east-1 --owners amazon --filters "Name=name,Values=al2023-ami-2023*-x86_64" "Name=state,Values=available" --query "sort_by(Images,&CreationDate)[-1].[ImageId,Name,CreationDate]" --output table
        
        Output >>
                ------------------------------------------------------
            |                   DescribeImages                   |
            +----------------------------------------------------+
            |  ami-0db1c5c6dc64eb019                             |
            |  al2023-ami-2023.12.20260817.0-kernel-6.12-x86_64  |
            |  2026-08-12T23:50:59.000Z                          |
            +----------------------------------------------------+

    step - 15 - Decide on Instance size - I'd recommend we examine the available instance types and pricing/limits, then choose something appropriate. use below command

        aws ec2 describe-instance-types --region us-east-1 --instance-types t3.small t3.medium t3.large --query "InstanceTypes[].[InstanceType,VCpuInfo.DefaultVCpus,MemoryInfo.SizeInMiB]" --output table

                        ----------------------------
                    |   DescribeInstanceTypes  |
                    +------------+----+--------+
                    |  t3.large  |  2 |  8192  |
                    |  t3.medium |  2 |  4096  |
                    |  t3.small  |  2 |  2048  |
                    +------------+----+--------+

        Our configuration is now
            Region          us-east-1
            VPC             vpc-0a0f89f8075ff0c57
            Subnet          subnet-017229d7a5d14863f
            AMI             ami-0db1c5c6dc64eb019
            Instance        t3.large
            Security Group  sg-0fd7498accef2485c

>> Milestone - 3 - create the EC2 IAM role. 
    
        This role will eventually allow the EC2 machine 
            a. To pull your Docker image from ECR and let Grafana access CloudWatch
            b. Avoid storing permanent AWS access keys on the production server

            EC2
            │
            └── IAM Role
                │
                ├── ECR permissions
                │
                └── CloudWatch permissions

    Step - 1 - Let's check whether you already have a suitable IAM role so we don't create unnecessary resources.
        aws iam list-roles --query "Roles[].[RoleName,Arn]" --output table --no-paginate

    step - 2 - So let's create a dedicated role for this production deployment rather than touching those existing roles. 
                We'll call it: demand-forecasting-ec2-role

    Step - 3 - create the trust policy (who can use the role)

    Step - 4 - Create a file called: ec2-trust-policy.json

    step - 5 - Now create the IAM role using the trust policy you just created.

        aws iam create-role --role-name demand-forecasting-ec2-role --assume-role-policy-document file://ec2-trust-policy.json

        >> Output 
                {
                    "Role": {
                        "Path": "/",
                        "RoleName": "demand-forecasting-ec2-role_v1",
                        "RoleId": "AROAR64OJ7GADOMQFTGTF",
                        "Arn": "arn:aws:iam::135053048192:role/demand-forecasting-ec2-role_v1",
                        "CreateDate": "2026-08-23T16:30:27+00:00",
                        "AssumeRolePolicyDocument": {
                            "Version": "2012-10-17",
                            "Statement": [
                                {
                                    "Effect": "Allow",
                                    "Principal": {
                                        "Service": "ec2.amazonaws.com"
                                    },
                                    "Action": "sts:AssumeRole"
                                }
                            ]
                        }
                    }
                }

    step - 6 - Let's attach the ECR read-only permission to our EC2 role.
        aws iam attach-role-policy --role-name demand-forecasting-ec2-role_v1 --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly

    step - 7 - Verify  if EC2 read only permession is attached to the role

        aws iam list-attached-role-policies --role-name demand-forecasting-ec2-role_v1 --output table
                        
                --------------------------------------------------------------------------------
                |                           ListAttachedRolePolicies                           |
                +------------------------------------------------------------------------------+
                ||                              AttachedPolicies                              ||
                |+------------+---------------------------------------------------------------+|
                ||  PolicyArn |  arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly   ||
                ||  PolicyName|  AmazonEC2ContainerRegistryReadOnly                           ||
                |+------------+--------------------------------------------

        Why this permission?
            The role needs permission to authenticate to ECR and pull the image. It does not need permission to push images.

    step - 6 - Attach cloud watch permessions
        We need Grafana on the EC2 to read:
            CloudWatch Metrics
            CloudWatch Logs

        aws iam attach-role-policy --role-name demand-forecasting-ec2-role_v1 --policy-arn arn:aws:iam::aws:policy/CloudWatchReadOnlyAccess

    step - 7 - Instance Profile - There is one AWS concept we need to understand before launching EC2:
        IAM Role ≠ Instance Profile - The instance profile is the container/wrapper AWS uses to attach the IAM role to an EC2 instance.
        So we will create instance profile

        aws iam create-instance-profile --instance-profile-name demand-forecasting-ec2-profile_v1

        >> output 
                {
                    "InstanceProfile": {
                    "Path": "/",
                    "InstanceProfileName": "demand-forecasting-ec2-profile_v1",
                    "InstanceProfileId": "AIPAR64OJ7GAELGLKEWQL",
                    "Arn": "arn:aws:iam::135053048192:instance-profile/demand-forecasting-ec2-profile_v1",
                    "CreateDate": "2026-08-23T16:37:17+00:00",
                    "Roles": []
                }
                 }

    step - 8 - We need to ut our IAM role inside it.
        aws iam add-role-to-instance-profile --instance-profile-name demand-forecasting-ec2-profile_v1 --role-name demand-forecasting-ec2-role_v1

    step - 9 - Verify

        aws iam get-instance-profile --instance-profile-name demand-forecasting-ec2-profile_v1 --query "InstanceProfile.Roles[].[RoleName,Arn]" --output table

        >> Output

            -----------------------------------------------------------------------------------------------
                |                                     GetInstanceProfile                                      |
                +------------------------------+--------------------------------------------------------------+
                |  demand-forecasting-ec2-role |  arn:aws:iam::135053048192:role/demand-forecasting-ec2-role_v1  |
                +------------------------------+--------------------------------------------------------------+

            EC2
                │
                ▼
                Instance Profile
                │
                ▼
                demand-forecasting-ec2-role
                │
                ├── ECR ReadOnly
                │
                └── CloudWatch ReadOnly

>> Milestone - 4 - Create EC2 Instance

    step - 1 - Create EC2 instance. We already have the required pieces:

                Component	               Value
                Region	                   us-east-1
                AMI	                       ami-0db1c5c6dc64eb019
                Instance type	           t3.large
                VPC	                       vpc-0a0f89f8075ff0c57
                Subnet	                   subnet-017229d7a5d14863f
                Security Group	           sg-0fd7498accef2485c
                IAM profile	               demand-forecasting-ec2-profile_v1

        Before we launch it, we'll make sure the EC2 gets a public IP, because you'll initially connect from your Windows machine using SSH.

        aws ec2 describe-subnets --region us-east-1 --subnet-ids subnet-017229d7a5d14863f --query "Subnets[0].[SubnetId,AvailabilityZone,CidrBlock,MapPublicIpOnLaunch]" --output table

                ------------------------------
                |       DescribeSubnets      |
                +----------------------------+
                |  subnet-017229d7a5d14863f  |
                |  us-east-1a                |
                |  172.31.0.0/20             |
                |  True                      |
                +----------------------------+

                | Thing          | Example         | Meaning                        |
                | -------------- | --------------- | ------------------------------ |
                | VPC CIDR       | `172.31.0.0/16` | Entire private network         |
                | Subnet CIDR    | `172.31.0.0/20` | A portion of that network      |
                | EC2 private IP | `172.31.x.x`    | EC2's internal address         |
                | EC2 public IP  | `54.x.x.x`      | Address used from the Internet |

    step - 2 - Launch the instance

        aws ec2 run-instances ^
            --image-id ami-0db1c5c6dc64eb019 ^
            --instance-type t3.large ^
            --subnet-id subnet-017229d7a5d14863f ^
            --security-group-ids sg-0fd7498accef2485c ^
            --iam-instance-profile Name=demand-forecasting-ec2-profile_v1 ^
            --associate-public-ip-address ^
            --region us-east-1 ^
            --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=demand-forecasting-prod}]"

    step - 3 - To get public and private address

        aws ec2 describe-instances --region us-east-1 --query "Reservations[].Instances[].[InstanceId,PrivateIpAddress,PublicIpAddress,State.Name]" --output table

            ----------------------------------------------------------------------
            |                          DescribeInstances                         |
            +----------------------+---------------+------------------+----------+
            |  i-04d5a03f6be8c9ad4 |  172.31.4.195 |  44.220.167.140  |  running |
            +----------------------+---------------+------------------+----------+

            44.220.167.140 → public IP, used to connect to the EC2 from your computer.
            172.31.4.195 → private IP, used for communication inside the AWS VPC.

    step - 4 - Before we try SSH, let's confirm that AWS actually attached our IAM instance profile to this EC2.

        aws ec2 describe-instances --instance-ids i-04d5a03f6be8c9ad4 --region us-east-1 --query "Reservations[0].Instances[0].IamInstanceProfile" --output table

            -----------------------------------------------------------------------------------------
            |                                   DescribeInstances                                   |
            +-----+---------------------------------------------------------------------------------+
            |  Arn|  arn:aws:iam::135053048192:instance-profile/demand-forecasting-ec2-profile_v1   |
            |  Id |  AIPAR64OJ7GAELGLKEWQL                                                          |
            +-----+---------------------------------------------------------------------------------+
    
    step - 5  - Next step: connect to the EC2
    
            Go to EC2 → Instances → select your instance → Connect and tell me what options you see on the Connect to instance screen. Then we'll do it step by step.

            1. EC2 Instance Connect → Public subnet access → Managed SSH keys - Click on connect
            2. Got error - Error establishing SSH connection to your instance. Try again later.
            3. In security group We allowed: TCP 22 . Source: 49.206.133.86/32 . That is correct for normal SSH directly from your laptop.
            4. But when you use EC2 Instance Connect from the AWS Console, AWS says the SSH traffic reaching the instance comes from the EC2 Instance Connect service, not directly from your laptop. The Security Group therefore needs to allow the AWS-managed EC2 Instance Connect prefix list.

    step - 6 - First, find the EC2 Instance Connect prefix list for us-east-1.

        aws ec2 describe-managed-prefix-lists --region us-east-1 --filters "Name=prefix-list-name,Values=com.amazonaws.us-east-1.ec2-instance-connect" --query "PrefixLists[].[PrefixListId,PrefixListName]" --output table

                --------------------------------------------------------------------------
                |                       DescribeManagedPrefixLists                       |
                +-----------------------+------------------------------------------------+
                |  pl-0e4bcff02b13bef1e |  com.amazonaws.us-east-1.ec2-instance-connect  |
                +-----------------------+------------------------------------------------+

    step - 7  - Now we need to allow EC2 Instance Connect to reach port 22 of our instance.

        aws ec2 authorize-security-group-ingress --group-id sg-0fd7498accef2485c --ip-permissions "IpProtocol=tcp,FromPort=22,ToPort=22,PrefixListIds=[{PrefixListId=pl-0e4bcff02b13bef1e}]" --region us-east-1
        >> Output

            {
            "Return": true,
            "SecurityGroupRules": [
                {
                    "SecurityGroupRuleId": "sgr-0cededcb8f5a70eeb",
                    "GroupId": "sg-0fd7498accef2485c",
                    "GroupOwnerId": "135053048192",
                    "IsEgress": false,
                    "IpProtocol": "tcp",
                    "FromPort": 22,
                    "ToPort": 22,
                    "PrefixListId": "pl-0e4bcff02b13bef1e",
                    "SecurityGroupRuleArn": "arn:aws:ec2:us-east-1:135053048192:security-group-rule/sgr-0cededcb8f5a70eeb"
                }
            ]
        }   

                    What this does

                        Previously we had:

                        Port 22
                        │
                        └── Your public IP
                            49.206.133.86/32

                        That allows your computer to SSH directly.

                        We're now adding:

                        Port 22
                        │
                        ├── Your IP
                        │   49.206.133.86/32
                        │
                        └── EC2 Instance Connect
                            pl-0e4bcff02b13bef1e

    step - 8 - After running it, verify:  
    
        aws ec2 describe-security-groups --group-ids sg-0fd7498accef2485c --region us-east-1 --query "SecurityGroups[0].IpPermissions" --output json. You should see two port-22 rules.

        >> output 
                    [
                        {
                            "IpProtocol": "tcp",
                            "FromPort": 22,
                            "ToPort": 22,
                            "UserIdGroupPairs": [],
                            "IpRanges": [
                                {
                                    "CidrIp": "49.206.133.86/32"
                                }
                            ],
                            "Ipv6Ranges": [],
                            "PrefixListIds": [
                                {
                                    "PrefixListId": "pl-0e4bcff02b13bef1e"
                                }
                            ]
                        }
                    ]

        Then go back to the EC2 Connect page and click Connect again.

    
    step - 9 -  Sucessfully connected to instance. Inside instance run

    step -10 - Run -  aws sts get-caller-identity
            output 
                {
                    "UserId": "AROAR64OJ7GAL7OMG3NES:i-02de20bdc4dcdd07a",
                    "Account": "135053048192",
                    "Arn": "arn:aws:sts::135053048192:assumed-role/demand-forecasting-ec2-role/i-02de20bdc4dcdd07a"
                }
    step - 11 - Next step: test ECR access 
        
        Now we want to prove that the EC2 can actually access your ECR repository using the role.

        aws ecr describe-repositories \
            --repository-names demand-forecasting \
            --region us-east-1

        >> output:-

                        "repositories": [
                    {
                        "repositoryArn": "arn:aws:ecr:us-east-1:135053048192:repository/demand-forecasting",
                        "registryId": "135053048192",
                        "repositoryName": "demand-forecasting",
                        "repositoryUri": "135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting",
                        "createdAt": "2026-08-19T10:44:52.545000+00:00",
                        "imageTagMutability": "MUTABLE",
                        "imageScanningConfiguration": {
                            "scanOnPush": false
                        },
                        "encryptionConfiguration": {
                            "encryptionType": "AES256"
                        }
                    }
                ]
            


    step - 12 - 
            Run - sudo dnf update -y
            Run - sudo dnf install -y docker

    Step - 13 - start docker - 

        sudo systemctl enable --now docker

    Step - 14 - verify docker version - 
        
        docker --version
        
        sudo systemctl status docker --no-pager

    step - 15 - Next: allow ec2-user to run Docker - Right now, Docker commands may require sudo because ec2-user isn't yet a member of 
                the docker group

        Run - sudo usermod -aG docker ec2-user

        Run - Refresh the group membership - newgrp docker

    step - 16 - Then verify the group membership using command 
        Run - groups
        Output >> ec2-user adm wheel systemd-journal 

    step - 17 -  Test Docker without sudo - 
        docker ps. 
        output >> CONTAINER ID   IMAGE   COMMAND   CREATED   STATUS   PORTS   NAMES

    step - 18 - log Docker into ECR

        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 135053048192.dkr.ecr.us-east-1.amazonaws.com
        
        output >> Login Success

    step - 19 - Next step: pull your production image

        docker pull 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:api-v2

    step - 20 - check using dokcer images
        
        docker images

    step - 21 - run - This tells us which port your API image exposes.
        docker inspect 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:api-v2 --format '{{.Config.ExposedPorts}}'
        >> output - 8000

    step - 22 - Next step: run the container 
        docker run -d \
            --name demand-forecasting-api \
            -p 8000:8000 \
            135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:api-v2


    step - 23 - run docker ps and docker logs demand-forecasting-api 
        
        We found issue saying Ec2 application will not connect to s3 becuase we had not given s3 permession to our Ec2


        1 - first check conetnts of s3 (run this in your local terminal) because of Ec2 has no list and getobject permession
            aws s3 ls s3://faang-ml-platform/forecast_data/

        2. Create the policy file directly on EC2

            cat > s3-read-policy.json <<'EOF'
            {
            "Version": "2012-10-17",
            "Statement": [
                {
                "Effect": "Allow",
                "Action": "s3:ListBucket",
                "Resource": "arn:aws:s3:::faang-ml-platform",
                "Condition": {
                    "StringLike": {
                    "s3:prefix": [
                        "forecast_data",
                        "forecast_data/*"
                    ]
                    }
                }
                },
                {
                "Effect": "Allow",
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::faang-ml-platform/forecast_data/*"
                }
            ]
            }
            EOF

        3. verify the file directly on Ec2 
            cat s3-read-policy.json

        4. Step 3 — Create the IAM policy (run this inside Ec2)

            aws iam create-policy --policy-name DemandForecastingS3ReadPolicy --policy-document file://s3-read-policy.json

            I got an error. because my Ec2 role has AmazonEC2ContainerRegistryReadOnly but it does not have permission to create IAM policies. So AWS correctly rejected: iam:CreatePolicy

            so we will proceed with crearting policy in my local laptop and attach to Ec2 role

        5. After creting policy in local I am attaching policy to Ec2 role 
            
            aws iam attach-role-policy --role-name demand-forecasting-ec2-role_v1 --policy-arn arn:aws:iam::135053048192:policy/DemandForecastingS3ReadPolicy"
                
        6 - Verify   
        
        aws iam list-attached-role-policies --role-name demand-forecasting-ec2-role_v1 --output table

        7. After successuly verifcation, we are moving back to Ec2 insatnce and creating conatiner
            - Ran the continer application started successfuly

        8 - Testing test the API from inside EC2
            - curl http://localhost:8000/health - Working

    step - 24 - The next step is to expose port 8000 securely through the EC2 Security Group and test the API from your laptop.

        Step 1 — Verify the EC2 public IP

            aws ec2 describe-instances --instance-ids i-04d5a03f6be8c9ad4 --region us-east-1 --query "Reservations[0].Instances[0].[PublicIpAddress,PrivateIpAddress,State.Name]" --output table

                    |DescribeInstances|
                    +-----------------+
                    |  32.199.139.75   |
                    |  172.31.4.195   |
                    |  running        |
                    +-----------------+

        step - 2 - verify laptop public Ip
            
            curl https://checkip.amazonaws.com - 49.206.133.86

        step - 3 - Now we'll allow only this IP to access your FastAPI port 8000. - Already done

        step - 4 - We want your laptop to reach the FastAPI application, not SSH
                So we'll add:
                        Port       : 8000
                        Protocol   : TCP
                        Source     : 49.206.133.86/32
                        Purpose    : FastAPI API access from your laptop


            aws ec2 authorize-security-group-ingress --group-id sg-0fd7498accef2485c --protocol tcp --port 8000 --cidr 49.206.133.86/32 --region us-east-1

        step -5 - curl http://32.199.139.75:8000/health (run this in terminal)
            
            output >>  {"status":"healthy","service":"Demand Forecasting API","version":"1.0.0","model_version":"1"}

        step - 6 - We had to give putobject permesison to our Ec2. So we modifed existing policy and updated   

            aws iam create-policy-version --policy-arn arn:aws:iam::135053048192:policy/DemandForecastingS3ReadPolicy --policy-document file://s3-read-policy.json --set-as-default


        step- 7 - ECR stores the image → EC2 downloads the image → Docker on EC2 runs the image as a container → the container runs your FastAPI API.
                And your laptop is accessing it through:

                        Laptop
                        │
                        │ http://100.53.55.3:8000
                        ▼
                        EC2
                        │
                        ▼
                        Docker Container
                        │
                        ▼
                        FastAPI

                        That's the deployment we have successfully built so far. ✅

                        What we've proven
                    EC2 instance running ✅
                    SSH / EC2 Instance Connect ✅
                    Docker installed and running ✅
                    ECR authentication ✅
                    Docker image pulled from ECR ✅
                    FastAPI container running ✅
                    /health working locally and externally ✅
                    Security Group configured for port 8000 ✅
                    EC2 IAM role working ✅
                    S3 read access ✅
                    SageMaker endpoint invocation ✅
                    Forecast generation ✅
                    Forecast result written back to S3 ✅
                    /forecast working end-to-end ✅

                    That's a real end-to-end AWS deployment, not just a Docker container sitting on EC2. 💪


>> Part - 2 - Move Promethus image to Ec2
    
    Step - 1 — Create the Docker network on EC2 ( This is needed because of container to container communication)
        In our case promethus shd talk to APi and Grafan to Promethus, so for this we need to have docker network
        For similar activity to do in loacl we use docker compose.

        docker network create demand-forecasting-network

    step - 2 - Then connect your existing API container to this network:
        
        docker network connect --alias api demand-forecasting-network demand-forecasting-api

        docker network connect demand-forecasting-network demand-forecasting-api
        
        The --alias api is important because your existing prometheus.yml has:targets: ["api:8000"]
        So Prometheus will be able to find your API using: api:8000


    Step - 3 — Verify

        docker network inspect demand-forecasting-network


    setp - 4 - get Prometheus image onto your laptop
        docker pull prom/prometheus:latest
        docker images prom/prometheus - To verify

    step - 5 - Tag this exact image for your existing ECR repository (Tag Prometheus for ECR)
        docker tag prom/prometheus:latest 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:prometheus-v1

    step - 6 - Push Prometheus to ECR
        docker push 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:prometheus-v1

    step - 7 - pull it on EC2
        docker pull 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:prometheus-v1


    step - 8 - Next we need to get your configuration files onto EC2.

                You currently have these on your laptop:

                        src/prometheus/
                        ├── prometheus.yml
                        ├── recording_rules.yml
                        └── alertmanager.yml

                Because your prometheus.yml references:

                rule_files:
                - "recording_rules.yml"

                we should mount the whole directory, not just prometheus.yml.

    step - 9 - Create the configuration directory on EC2

        mkdir -p ~/prometheus or /home/ec2-user/prometheus -> make directory. # the ~ means "my current user's home directory."
        # There fore ~/prometheus is same as /home/ec2-user/prometheus

        Why /home/ -? 
        EC2 instance has a Linux user: ec2-user
        When you're logged in as that user, its home directory is: /home/ec2-user
        You can verify this on EC2 - echo $HOME
        you will get - /home/ec2-user
            
    step - 10 - Verify if difrectory exists - 
    
       ls -la ~/prometheus 

    Step - 11 — Copy the Prometheus configuration from your laptop

        scp src\prometheus\prometheus.yml ec2-user@32.199.139.75:/home/ec2-user/prometheus/
        scp src\prometheus\recording_rules.yml ec2-user@32.199.139.75:/home/ec2-user/prometheus/
        scp src\prometheus\alertmanager.yml ec2-user@32.199.139.75:/home/ec2-user/prometheus/

    The above commands didnt work in my laptop becuase scp is not installed.
    so we are directly creating files in ec2

    step - 12 - Create prometheus.yml in Ec2

        cat > ~/prometheus/prometheus.yml <<'EOF'
        global:
        scrape_interval: 15s

        rule_files:
        - "recording_rules.yml"

        scrape_configs:
        - job_name: "demand-forecasting-api"
        static_configs:
            - targets: ["api:8000"]
        EOF

    step - 13 - Verify - 
       cat ~/prometheus/prometheus.yml

    step - 14 - 
            cat > ~/prometheus/recording_rules.yml <<'EOF'
            groups:
            - name: forecast_recording_rules
                interval: 30s
                rules:
                - record: forecast_request_duration_seconds:p95
                    expr: |
                    histogram_quantile(
                        0.95,
                        rate(forecast_request_duration_seconds_bucket[5m])
                    )

            - name: forecast_alerts
                rules:
                - alert: HighForecastLatency
                    expr: forecast_request_duration_seconds:p95 > 100
                    for: 1m
                    labels:
                    severity: warning
                    annotations:
                    summary: "High forecast API latency"
                    description: "P95 forecast latency has been above 100 seconds for 1 minute."
            EOF

    step -15 - Verify - 
    
       cat ~/prometheus/recording_rules.yml

    step - 16 - Let's validate the Prometheus configuration before starting the container. 
                This can catch YAML/configuration mistakes without affecting your API.

        docker run --rm \
            --entrypoint promtool \
            -v ~/prometheus:/etc/prometheus:ro \
            135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:prometheus-v1 \
            check config /etc/prometheus/prometheus.yml

        This is actually a very good production practice

    step - 17 - Run the Prometheus container.

            docker run -d \
            --name prometheus \
            --network demand-forecasting-network \
            -p 9090:9090 \
            -v ~/prometheus:/etc/prometheus:ro \
            135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:prometheus-v1 \
            --config.file=/etc/prometheus/prometheus.yml # explicitly saying prometeus to use this config file

    step - 18 - Check Prometheus logs - docker logs prometheus

    step - 19 - Check Prometheus targets - 
       curl http://localhost:9090/api/v1/targets
        
        This is important because your configuration says:
                targets:
                  - api:8000
        We want Prometheus to report the API target as UP.

>> Part -3 - Move Grafana image to Ec2

    step - 1  - Pull images in local
        
        docker pull grafana/grafana:12.1.1
        
        docker images prom/prometheus - To verify

    step - 2  Tag it for your existing ECR repository
            
        docker tag grafana/grafana:12.1.1 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:grafana-v1

    step - 3 - Push 
            
        docker push 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:grafana-v1

    step - 4 - Pull iages form ECR to Ec2
            
        docker pull 135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:grafana-v1

    step - 5 verify in Ec2 
            
        docker images

    step - 6 Run the continer in Ec2
        docker run -d \
            --name grafana \
            --network demand-forecasting-network \
            -p 3000:3000 \
            135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:grafana-v1

    setp - 7 - Add rule to security group to alllow communcition to grafana (3000) and Promethus (9090)
        
        aws ec2 authorize-security-group-ingress --group-id sg-0fd7498accef2485c --protocol tcp --port 3000 --cidr 49.206.133.86/32 --region us-east-1

        aws ec2 authorize-security-group-ingress --group-id sg-0fd7498accef2485c --protocol tcp --port 9090 --cidr 49.206.133.86/32 --region us-east-1

    setup - 8 - Now we forgot to move grafana backup to Ec2 now we are doing it

        Step - 1 — Inspect both volumes

            docker volume inspect grafana-data
            docker volume inspect grafana_data
            We dont know which one is latest

        step - 2 - Check which volume your old Grafana container uses
            
            docker inspect intelligentdemandforecastingplatform-grafana-1 --format="{{json .Mounts}}" (using this commad as conatiner was stil runng)

            By using above command we knew grafana_data is latest one

        Step 3 — Stop the old local Grafana
            
            docker stop intelligentdemandforecastingplatform-grafana-1

        step - 4 - Create a backup of grafana_data

            docker run --rm ^
                -v grafana_data:/source:ro ^
                -v "%cd%":/backup ^
                alpine ^
                tar czf /backup/grafana_data_backup.tar.gz -C /source .

            This creates: D:\ML Algorithms\ML Project\Intelligent Demand Forecasting Platform\grafana_data_backup.tar.gz
            it contains the contents of: 
                                grafana_data
                                    ↓
                                /var/lib/grafana

        step - 5 - verify the backup file exists and check its size before we transfer anything.
            
            dir grafana_data_backup.tar.gz

        step - 6 - Upload backup to s3
            
            aws s3 cp "grafana_data_backup.tar.gz" s3://faang-ml-platform/grafana-backup/grafana_data_backup.tar.gz --region us-east-1

        step - 7 - Verify
            aws s3 ls s3://faang-ml-platform/grafana-backup/ --region us-east-1

        step - 8 - On Ec2 download the backup
            
            aws s3 cp s3://faang-ml-platform/grafana-backup/grafana_data_backup.tar.gz ~/grafana_data_backup.tar.gz --region us-east-1

            Ec2 is not able to download the backup due to policy  problem

        step - 9 - Let's check the current policy before changing anything

            aws iam get-policy-version ^
            --policy-arn arn:aws:iam::135053048192:policy/DemandForecastingS3ReadPolicy ^
            --version-id v2 ^
            --query "PolicyVersion.Document" ^
            --output json

        step - 10 - Update s3-read-policy.json(in local)

        Step - 11 - Create the new policy version

            aws iam create-policy-version ^
                --policy-arn arn:aws:iam::135053048192:policy/DemandForecastingS3ReadPolicy ^
                --policy-document file://s3-read-policy.json ^
                --set-as-default
                                
            You should get something like:
                "VersionId": "v3",
                "IsDefaultVersion": true

        step - 12 -  Verify

            aws iam get-policy ^
            --policy-arn arn:aws:iam::135053048192:policy/DemandForecastingS3ReadPolicy ^
            --query "Policy.DefaultVersionId"

            it shd say verios v3

        Step - 13 - Try the download again on EC2

        step - 14 - Verify 
        
           - ls -lh ~/grafana_data_backup.tar.gz


        step - 15 - Check whether the old volume exists
            
            docker volume ls | grep grafana # gref grafana shows only lines conting word grafana

        Step - 16 - Create the a new volume on EC2

            docker volume create grafana_data

        step - 17 - verify
            
            docker volume ls

        Step - 18 - Restore the backup into grafana_data

            docker run --rm -v grafana_data:/source -v ~/grafana_data_backup.tar.gz:/backup.tar.gz:ro alpine tar xzf /backup.tar.gz -C/source

        step - 19 - Verfiy  
            docker run --rm \
            -v grafana_data:/var/lib/grafana:ro \
            alpine \
            ls -la /var/lib/grafana

        step - 20 - Stop Grafana
            docker stop grafana

        step -21 - Remove only the container
                docker rm grafana

        step - 22 Start Grafana with the restored volume

            docker run -d \
                --name grafana \
                --network demand-forecasting-network \
                -p 3000:3000 \
                -v grafana_data:/var/lib/grafana \
                135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:grafana-v1

        step - 24 - docker ps

>> Create a SageMaker invoke policy

    step -1 - Create the IAM policy

      aws iam create-policy ^
        --policy-name DemandForecastingSageMakerInvokePolicy ^
        --policy-document file://sagemaker-invoke-policy.json
    
    setp -2 - Attach it to your EC2 role
      aws iam attach-role-policy ^
        --role-name demand-forecasting-ec2-role_v1 ^
        --policy-arn arn:aws:iam::135053048192:policy/DemandForecastingSageMakerInvokePolicy

    step -3 - 
      aws iam list-attached-role-policies ^
        --role-name demand-forecasting-ec2-role_v1 ^
        --output table
    

>> To stop the insatnce

    step - 1
        aws ec2 describe-instances --region us-east-1 --filters "Name=ip-address,Values=32.199.139.75" --query "Reservations[].Instances[].InstanceId" --output text

    Step 2 — Stop that actual instance
        aws ec2 stop-instances --instance-ids i-04d5a03f6be8c9ad4 --region us-east-1

    step- 3 - vrify
        aws ec2 describe-instances --instance-ids i-04d5a03f6be8c9ad4 --region us-east-1 --query "Reservations[].Instances[].State.Name" --output text


>> To intergrate the cloud watch

step - 1 - Create the IAM policy
    aws iam create-policy ^
    --policy-name DemandForecastingCloudWatchLogsWritePolicy ^
    --policy-document file://cloudwatch-logs-policy.json

step - 2 - Attach it to the role

    aws iam attach-role-policy ^
        --role-name demand-forecasting-ec2-role_v1 ^
        --policy-arn arn:aws:iam::135053048192:policy/DemandForecastingCloudWatchLogsWritePolicy

step - 3 - Stopped the existing running conatier and remove it

    docker run -d \
            --name demand-forecasting-api \
            -p 8000:8000 \
            --restart unless-stopped \
            --log-driver=awslogs \
            --log-opt awslogs-region=us-east-1 \
            --log-opt awslogs-group=/demand-forecasting/api \
            --log-opt awslogs-create-group=true \
            --log-opt awslogs-stream=api \
            135053048192.dkr.ecr.us-east-1.amazonaws.com/demand-forecasting:api-v2

step - 4 - Connect to demand-forecasting-network

    docker network connect --alias api demand-forecasting-network demand-forecasting-api

step - 5 - Verify Docker is actually using CloudWatch
    docker inspect demand-forecasting-api --format '{{json .HostConfig.LogConfig}}'

step - 6 - Check CloudWatch. From your local machine or EC2, run
    aws logs describe-log-groups \
    --log-group-name-prefix /demand-forecasting/api \
    --region us-east-1

        output = 
                    {
                        "logGroups": [
                            {
                                "logGroupName": "/demand-forecasting/api",
                                "creationTime": 1787480441935,
                                "metricFilterCount": 0,
                                "arn": "arn:aws:logs:us-east-1:135053048192:log-group:/demand-forecasting/api:*",
                                "storedBytes": 0,
                                "logGroupClass": "STANDARD",
                                "logGroupArn": "arn:aws:logs:us-east-1:135053048192:log-group:/demand-forecasting/api",
                                "deletionProtectionEnabled": false
                            }
                        ]
                    }
step - 7 - We can see storedBytes: 0. That means the group was created, but we haven't confirmed that log events are arriving yet.

step - 8  -  Check the log stream - 
    aws logs describe-log-streams --log-group-name /demand-forecasting/api --region us-east-1
       Output:-
            {
                "logStreams": [
                    {
                        "logStreamName": "api",
                        "creationTime": 1787480441971,
                        "firstEventTimestamp": 1787480449516,
                        "lastEventTimestamp": 1787480451242,
                        "lastIngestionTime": 1787480452004,
                        "uploadSequenceToken": "49039859683677502189459545179569786433409840262696494639",
                        "arn": "arn:aws:logs:us-east-1:135053048192:log-group:/demand-forecasting/api:log-stream:api",
                        "storedBytes": 0
                    }
                ]
            }

Step - 9  — Actually read the logs
            aws logs get-log-events \
            --log-group-name /demand-forecasting/api \
            --log-stream-name api \
            --region us-east-1 \
            --limit 20

>> TO check how Prometheus was started

step - 1 - docker inspect prometheus --format '{{json .Mounts}}'

output >>  "/home/ec2-user/prometheus":"/etc/prometheus"

step - 2 - docker inspect prometheus --format '{{range .Mounts}}{{println .Source "->" .Destination}}{{end}}'

output >>  "/home/ec2-user/prometheus":"/etc/prometheus"

step - 3 - docker exec prometheus wget -qO- http://demand-forecasting-api:8000/metrics 




    So remember this
Communication	Docker internal network?
Laptop → EC2 → API	❌ No
Laptop → EC2 → Grafana	❌ No
Laptop → EC2 → Prometheus	❌ No
Prometheus → API	✅ Yes
Grafana → Prometheus	✅ Yes
Grafana → API directly	✅ Yes, if using container name

The port mappings (8000:8000, 3000:3000, 9090:9090) are for exposing containers through the EC2 host.

The Docker network (demand-forecasting-network) is for communication between containers.





            






                    AWS
                     │
              ┌──────▼──────┐
              │     VPC     │
              │ 172.31/16   │
              └──────┬──────┘
                     │
              Public Subnet
              us-east-1a
                     │
              ┌──────▼──────┐
              │     EC2     │
              │             │
              │ Docker      │
              │ ├── API     │
              │ ├── Prom    │
              │ └── Grafana │
              └─────────────┘
                     │
              Security Group
                     │
             controls traffic