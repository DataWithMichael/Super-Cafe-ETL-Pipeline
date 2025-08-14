#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <aws_profile> <your_name>"
  exit 1
fi

aws_profile="$1"
your_name="$2"

deployment_bucket="${your_name}-deployment-bucket"

echo ""
echo "Deploying deployment bucket stack..."
aws cloudformation deploy \
  --stack-name "${deployment_bucket}" \
  --template-file deployment-bucket-stack.yml \
  --region eu-west-1 \
  --capabilities CAPABILITY_IAM \
  --profile "${aws_profile}" \
  --parameter-overrides YourName="${your_name}"

echo ""
echo "Deploying raw data bucket stack..."
aws cloudformation deploy \
  --stack-name "${your_name}-etl-pipeline" \
  --template-file s3-bucket.yml \
  --region eu-west-1 \
  --capabilities CAPABILITY_NAMED_IAM \
  --profile "${aws_profile}" \
  --parameter-overrides TeamName="${your_name}"

echo ""
echo "Deployment complete!"
