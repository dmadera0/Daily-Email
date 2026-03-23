import json
import logging

import boto3

from email_builder import build_email_html
from news import get_top_news
from quotes import get_motivational_quote
from weather import get_weather

# ---------------------------------------------------------------------------
# Logging — all logger.info / logger.error calls appear in CloudWatch Logs
# ---------------------------------------------------------------------------
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# AWS clients — initialised OUTSIDE the handler so Lambda can reuse them
# across warm invocations (saves ~50ms per call)
# ---------------------------------------------------------------------------
secrets_client = boto3.client("secretsmanager")
dynamodb = boto3.resource("dynamodb")
ses_client = boto3.client("ses", region_name="us-east-1")

# ---------------------------------------------------------------------------
# Configuration — change these to match your AWS setup
# ---------------------------------------------------------------------------
SECRET_NAME = "daily-emailer/api-keys"
DYNAMODB_TABLE = "daily-emailer-recipients"
SES_SENDER_NAME = "Daily Emailer"
SES_SENDER_EMAIL = "your-verified-email@example.com"  # MUST be SES-verified
EMAIL_SUBJECT = "☀️ Your Daily Briefing"
WEATHER_CITY = "Los Angeles"


def get_api_keys() -> dict:
    """Retrieve all API keys from AWS Secrets Manager in a single call."""
    logger.info(f"Fetching secrets from: {SECRET_NAME}")
    response = secrets_client.get_secret_value(SecretId=SECRET_NAME)
    return json.loads(response["SecretString"])


def get_recipients() -> list[dict]:
    """
    Scan DynamoDB for all recipients where active == True.

    NOTE: scan() reads the full table — fine for small lists.
    At scale, replace with a GSI query for better performance.
    """
    table = dynamodb.Table(DYNAMODB_TABLE)
    response = table.scan(
        FilterExpression="active = :val",
        ExpressionAttributeValues={":val": True},
    )
    return response.get("Items", [])


def send_email(to_address: str, to_name: str, html_body: str) -> None:
    """Send a single HTML email via AWS SES."""
    ses_client.send_email(
        Source=f"{SES_SENDER_NAME} <{SES_SENDER_EMAIL}>",
        Destination={"ToAddresses": [f"{to_name} <{to_address}>"]},
        Message={
            "Subject": {"Data": EMAIL_SUBJECT, "Charset": "UTF-8"},
            "Body": {"Html": {"Data": html_body, "Charset": "UTF-8"}},
        },
    )


def handler(event, context):
    """
    Lambda entry point. Called by EventBridge on cron schedule.

    Args:
        event:   EventBridge scheduled event payload (dict)
        context: Lambda runtime context (LambdaContext object)

    Returns:
        dict with statusCode and body (standard Lambda response shape)
    """
    logger.info("Daily emailer Lambda invoked")
    logger.info(f"Event: {json.dumps(event)}")

    try:
        # 1. Credentials
        keys = get_api_keys()

        # 2. Fetch content from external APIs
        logger.info("Fetching weather...")
        weather = get_weather(keys["OPENWEATHER_API_KEY"], city=WEATHER_CITY)

        logger.info("Fetching news...")
        news = get_top_news(keys["NEWSAPI_KEY"])

        logger.info("Fetching quote...")
        quote = get_motivational_quote()

        # 3. Build HTML email body once (reused for every recipient)
        html_body = build_email_html(weather, news, quote)

        # 4. Load recipients and send
        recipients = get_recipients()
        logger.info(f"Sending to {len(recipients)} active recipients")

        sent, failed = 0, 0
        for recipient in recipients:
            try:
                send_email(
                    to_address=recipient["email"],
                    to_name=recipient.get("name", "Friend"),
                    html_body=html_body,
                )
                sent += 1
                logger.info(f"Sent → {recipient['email']}")
            except Exception as exc:
                failed += 1
                logger.error(f"Failed → {recipient['email']} — {exc}")

        summary = f"Done. Sent: {sent} | Failed: {failed}"
        logger.info(summary)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": summary}),
        }

    except Exception as exc:
        logger.error(f"Lambda execution failed: {exc}", exc_info=True)
        raise  # Re-raising marks the invocation FAILED in CloudWatch metrics
