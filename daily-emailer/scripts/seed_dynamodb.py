"""
Seed script — populates the DynamoDB recipients table with test data.

Usage:
    python scripts/seed_dynamodb.py

Requires:
    - AWS credentials configured (aws configure or environment variables)
    - The 'daily-emailer-recipients' table already created in DynamoDB
"""

import boto3

# ── Configure these before running ────────────────────────────────────────
TABLE_NAME = "daily-emailer-recipients"
REGION = "us-east-1"

RECIPIENTS = [
    {"email": "dmadera0@gmail.com", "name": "Daniel", "active": True},
    {"email": "d.madera@sportradar.com", "name": "Daniel - Work", "active": True},
    # Add more recipients here — set active=False to disable without deleting
]
# ──────────────────────────────────────────────────────────────────────────


def seed():
    dynamodb = boto3.resource("dynamodb", region_name=REGION)
    table = dynamodb.Table(TABLE_NAME)

    print(f"Seeding {len(RECIPIENTS)} recipients into '{TABLE_NAME}'...")

    for recipient in RECIPIENTS:
        table.put_item(Item=recipient)
        status = "active" if recipient["active"] else "inactive"
        print(f"  ✓ {recipient['email']} ({recipient['name']}) — {status}")

    print("Done.")


if __name__ == "__main__":
    seed()
