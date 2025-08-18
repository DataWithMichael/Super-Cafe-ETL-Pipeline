#!/bin/sh
set -eu

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 <aws_profile> <team_name> [region]"
  exit 1
fi

# Parameters
aws_profile=$1
team_name=$2
region=${3:-eu-west-1}
deployment_bucket="${team_name}-deployment-bucket"

# Check if deployment bucket exists
echo ""
echo "Checking if deployment bucket '$deployment_bucket' exists..."
if ! aws s3api head-bucket --bucket "$deployment_bucket" --profile "$aws_profile" 2>/dev/null; then
    echo "Deployment bucket not found. Creating via CloudFormation..."
    aws cloudformation deploy \
        --stack-name "$deployment_bucket" \
        --template-file deployment-bucket-stack.yml \
        --region "$region" \
        --capabilities CAPABILITY_IAM \
        --profile "$aws_profile" \
        --parameter-overrides \
            TeamName="$team_name"
else
    echo "Deployment bucket already exists. Skipping bucket creation."
fi

# Optional pip install for Lambda dependencies
if [ -z "${SKIP_PIP_INSTALL:-}" ]; then
    echo ""
    echo "Installing Python dependencies for Lambda..."
    python3 -m pip install \
        --platform manylinux2014_x86_64 \
        --target=./src \
        --implementation cp \
        --python-version 3.12 \
        --only-binary=:all: \
        --upgrade -r requirements-lambda.txt
else
    echo ""
    echo "Skipping pip install..."
fi

# Encode EC2 userdata
if [ -f userdata ]; then
    echo ""
    echo "Encoding EC2 userdata..."
    ec2_userdata=$(base64 -w 0 userdata) #-w 0 ensures no line breaks
else
    echo ""
    echo "No userdata file found. Skipping userdata encoding."
    ec2_userdata=""
fi

# Package ETL template
echo ""
echo "Packaging ETL CloudFormation template..."
aws cloudformation package \
    --template-file etl-stack.yml \
    --s3-bucket $deployment_bucket \
    --output-template-file etl-stack-packaged.yml \
    --profile $aws_profile \
    --region $region

# Deploy packaged CloudFormation stack
echo ""
echo "Deploying ETL CloudFormation stack..."
aws cloudformation deploy \
    --stack-name "${team_name}-store-etl-pipeline" \
    --template-file etl-stack-packaged.yml \
    --capabilities CAPABILITY_IAM \
    --profile "$aws_profile" \
    --region "$region" \
    --parameter-overrides \
        TeamName="$team_name" \
        EC2UserData="$ec2_userdata"

echo ""
echo "ETL Deployment complete!"
echo ""
