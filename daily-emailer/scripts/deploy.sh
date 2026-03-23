#!/bin/bash
# Deploys the zipped Lambda package to AWS.
# Prerequisites: AWS CLI configured, daily-emailer.zip exists.
# Run: bash scripts/deploy.sh

set -e

FUNCTION_NAME="daily-emailer"
REGION="us-east-1"

echo "→ Packaging..."
bash scripts/package.sh

echo "→ Deploying to Lambda function: $FUNCTION_NAME..."
aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file fileb://daily-emailer.zip \
    --region "$REGION"

echo "✓ Deployed successfully."
echo "  Check logs at: https://console.aws.amazon.com/cloudwatch/home?region=$REGION#logsV2:log-groups/log-group/\$252Faws\$252Flambda\$252F$FUNCTION_NAME"
