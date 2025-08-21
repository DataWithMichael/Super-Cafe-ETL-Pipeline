### PowerShell Script to deploy S3 bucket, lambda and ETL stack, and optional EC2 userdata
### Compatible with local src directory and optional pip install

# Exit script on any error
$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

#### CONFIGURATION SECTION ####
# Parameters
$aws_profile=$args[0] # e.g. sot-academy
$team_name=$args[1]    # e.g. ana-lattex
$region = if ($args.count -ge 3) { $args[2]} else {"eu-west-1"}
$deployment_bucket="$team_name-deployment-bucket"
#### CONFIGURATION SECTION ####

Write-Output ""
Write-Output "Checking if deployment bucket '$deployment_bucket' exists..."

# Run the command and capture the exit code instead of redirecting in-line
$bucket_check = aws s3api head-bucket --bucket $deployment_bucket --profile $aws_profile -ErrorAction SilentlyContinue

if (-not $bucket_check) {
    Write-Output "Deployment bucket not found. Creating via CloudFormation..."
    aws cloudformation deploy `
        --stack-name $deployment_bucket `
        --template-file deployment-bucket-stack.yml `
        --region $region `
        --capabilities CAPABILITY_IAM `
        --profile $aws_profile `
        --parameter-overrides TeamName=$team_name
} else {
    Write-Output "Deployment bucket already exists. Skipping bucket creation."
}

if (LASTEXITCODE -ne 0) {
    Write-Output "Deployment bucket not found, creating via CloudFormation..."
    aws cloudformation deploy `
        --stack-name $deployment_bucket `
        --template-file deployment-bucket-stack.yml `
        --region $region `
        --capabilities CAPABILITY_IAM `
        --profile $aws_profile `
        --parameter-overrides `
            TeamName="$team_name"
} else {
    Write-Output "Deployment bucket already exists. Skipping bucket creation."
}

# Optional pip install for Lambda dependencies
if (-not $env:SKIP_PIP_INSTALL) {
    Write-Output ""
    Write-Output "Installing Python dependencies for Lambda..."
    python -m pip install `
        --platform manylinux2014_x86_64 `
        --target=./src `
        --implementation cp `
        --python-version 3.12 `
        --only-binary=:all: `
        --upgrade -r requirements-lambda.txt
} else {
    Write-Output ""
    Write-Output "Skipping pip install"
}

# Encode EC2 userdata
$ec2_userdata_file ="./userdata" # path to cloud-init userdata script
if (Test-Path $ec2_userdata_file) {
    Write-Output "Encoding EC2 userdata..."
    $ec2_userdata = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes((Get-Content $ec2_userdata_file -Raw)))  
    $ec2_userdata = $ec2_userdata.Trim() # remove stray newlines
} else {
    Write-Output "No userdata file found, skipping EC2 UserData..."
    $ec2_userdata = ""
}

# Package ETL template
Write-Output ""
Write-Output "Packaging ETL CloudFormation template..."
aws cloudformation package `
    --template-file etl-stack.yml `
    --s3-bucket $deployment_bucket `
    --output-template-file etl-stack-packaged.yml `
    --profile $aws_profile `
    --region $region

# Deploy packaged CloudFormation stack
Write-Output ""
Write-Output "Deploying ETL CloudFormation stack..."
aws cloudformation deploy `
    --stack-name "$team_name-store-etl-pipeline" `
    --template-file etl-stack-packaged.yml `
    --region $region `
    --capabilities CAPABILITY_IAM `
    --profile $aws_profile `
    --parameter-overrides `
        TeamName="$team_name" `
        EC2UserData="$ec2_userdata"

Write-Output ""
Write-Output "...All Done!"
Write-Output ""
