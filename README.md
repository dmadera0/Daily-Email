# Daily Emailer — AWS Serverless

A serverless daily email digest built on AWS Lambda, EventBridge, DynamoDB, SES, and Secrets Manager.

Sends a morning email with weather, top news headlines, and a motivational quote to a list of recipients stored in DynamoDB.

## Architecture

```
EventBridge (cron) → Lambda → DynamoDB (recipients)
                            → Secrets Manager (API keys)
                            → OpenWeatherMap API
                            → NewsAPI.org
                            → ZenQuotes.io
                            → SES → Recipients
```

## Prerequisites

- Python 3.12+
- AWS CLI configured (`aws configure`)
- AWS account with access to Lambda, DynamoDB, SES, Secrets Manager, EventBridge, IAM
- Free API keys from:
  - [OpenWeatherMap](https://openweathermap.org/api) (free tier)
  - [NewsAPI](https://newsapi.org/) (free tier)

## Setup — Step by Step

### 1. Create DynamoDB table

In AWS Console → DynamoDB → Create Table:
- Table name: `daily-emailer-recipients`
- Partition key: `email` (String)

Then seed it:
```bash
python scripts/seed_dynamodb.py
```

### 2. Store API keys in Secrets Manager

AWS Console → Secrets Manager → Store new secret → Other type:
- Secret name: `daily-emailer/api-keys`
- Key/value pairs:
  - `OPENWEATHER_API_KEY` → your key
  - `NEWSAPI_KEY` → your key

### 3. Verify your sender email in SES

AWS Console → SES → Verified Identities → Create Identity → Email Address

Check your inbox and click the verification link.

### 4. Create the Lambda function

AWS Console → Lambda → Create Function:
- Runtime: Python 3.12
- Architecture: x86_64
- Handler: `index.handler`
- Timeout: 30 seconds
- Memory: 256 MB

Update `SES_SENDER_EMAIL` in `lambda/index.py` to your verified email.

### 5. Attach IAM policy

Attach `iam/lambda-policy.json` as an inline policy to your Lambda's execution role.

### 6. Package and deploy

```bash
bash scripts/deploy.sh
```

### 7. Create EventBridge rule

AWS Console → EventBridge → Rules → Create Rule:
- Schedule: `cron(0 14 * * ? *)` — fires at 7am Pacific (14:00 UTC) daily
- Target: your Lambda function

### 8. Test

In Lambda console, create a test event with any JSON payload and click Test.
Check CloudWatch Logs for output.

## Running tests locally

```bash
pip install pytest
pytest tests/ -v
```

## Project structure

```
daily-emailer/
├── lambda/          # All Lambda source code
├── iam/             # IAM policy JSON
├── scripts/         # Package, deploy, and seed scripts
├── tests/           # Unit tests (mocked, no AWS calls)
├── .env.example     # Local env var template
└── README.md
```

## Cost

Approximately $0.40/month (Secrets Manager only). All other services stay within AWS free tier for this usage pattern.
