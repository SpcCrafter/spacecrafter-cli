# spacecrafter-cli


## How to install?

1. Clone a repository and move to it
   ```
   git clone https://github.com/SpcCrafter/spacecrafter-cli.git
   cd spacecrafter-cli
   ```
1. Install the CLI of the tool, execute the command:
   ```
   $ pip install -e .
   ```
  This command installs the tool in developer mode, allowing you to work with it without reinstalling it after each change.

## How to use?

Prerequisites:
- Create a dev env of API and DB by the following runbook - https://github.com/SpcCrafter/spacecrafter-api/blob/main/README.md
- Do the following steps [here](#create-iam-role)

1. Use `spc --help` to see all available commands
2. Signup with `spc signup USERNAME EMAIL` command
3. Login with `spc login USERNAME`
4. Set AWS credentials with `spc set-aws-credentials` command where you need to provide Access Keys which will be hidden as on the following screenshot :
<img width="405" alt="image" src="https://github.com/SpcCrafter/spacecrafter-cli/assets/71873090/428a8edc-872c-4139-bfb4-b1b11c7318c3">

5. Create a container with `spc create-container CONTAINER_NAME --cpu 0.2 --storage 2 --image IMAGE_NAME` command where you can provide either a local image or a docker hub image
6. Connect to a container with SSH by using `spc connect-container CONTAINER_NAME`


## Create IAM role

1. Go to your AWS account
2. Create an IAM policy with the following permissions
   ```json
    {
    	"Version": "2012-10-17",
    	"Statement": [
    		{
    			"Effect": "Allow",
    			"Action": [
    				"ec2:CreateKeyPair",
    				"ec2:DescribeKeyPairs",
    				"ec2:DeleteKeyPair",
    				"ec2:CreateSecurityGroup",
    				"ec2:DescribeSecurityGroups",
    				"ec2:DeleteSecurityGroup",
    				"ec2:AuthorizeSecurityGroupIngress",
    				"ec2:RevokeSecurityGroupIngress",
    				"ec2:RunInstances",
    				"ec2:DescribeInstances",
    				"ec2:TerminateInstances",
    				"ec2:DescribeImages",
    				"ec2:CreateTags",
    				"ec2:DeleteTags",
    				"ec2:DescribeTags"
    			],
    			"Resource": "*"
    		},
    		{
    			"Effect": "Allow",
    			"Action": [
    				"s3:CreateBucket",
    				"s3:PutObject",
    				"s3:GetObject",
    				"s3:ListBucket"
    			],
    			"Resource": [
    				"arn:aws:s3:::*"
    			]
    		},
    		{
    			"Effect": "Allow",
    			"Action": [
    				"kms:Encrypt",
    				"kms:Decrypt",
    				"kms:DescribeKey",
    				"kms:CreateKey",
    				"kms:CreateAlias"
    			],
    			"Resource": "*"
    		}
    	]
    }
   ```

4. Create an IAM User with newly created IAM policy attached
5. Go to User > Security Credentials Section > Access keys and create a new Access Key
   <img width="1374" alt="image" src="https://github.com/SpcCrafter/spacecrafter-cli/assets/71873090/7c4d9c7b-a735-49de-8db3-5887cff4bddb">

7. Download a .csv file to retrieve access keys to use when provide AWS credentials for a container management 
   <img width="1456" alt="image" src="https://github.com/SpcCrafter/spacecrafter-cli/assets/71873090/510b22cb-d7e9-4563-b57e-7d3bab7b8daa">

