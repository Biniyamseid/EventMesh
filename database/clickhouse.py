
from clickhouse_driver import Client
from uuid import uuid4
from datetime import datetime, timezone

# client = Client('localhost')
client = Client('resend_webhook_clickhouse')
# -----------------------------------

def create_database():
    client.execute('DROP DATABASE IF EXISTS webhook')
    client.execute('CREATE DATABASE IF NOT EXISTS webhook')

def create_table():
    client.execute('DROP TABLE IF EXISTS webhook.payloads')
    client.execute('''
        CREATE TABLE IF NOT EXISTS webhook.payloads (
            id UUID,
            sender String,
            recipient String,
            subject String,
            email_id String,
            event_type String,
            created_at DateTime('UTC')
        ) ENGINE = MergeTree()
        ORDER BY created_at
    ''')

def insert_payload(payload):
    # Parse the payload
    sender = payload["data"].get("from")
    recipient = payload["data"].get("to")[0] if payload["data"].get("to") else None
    subject = payload["data"].get("subject")
    email_id = payload["data"].get("email_id")
    event_type = payload.get("type")

    # Check if sender is present
    if not sender:
        raise ValueError("Payload must include a 'from' value")

    # Generate id and created_at values
    id = uuid4()
    created_at = datetime.fromisoformat(payload["created_at"].replace("Z", "+00:00"))

    # Insert into database
    client.execute(
        'INSERT INTO webhook.payloads (id, sender, recipient, subject, email_id, event_type, created_at) VALUES',
        [(id, sender, recipient, subject, email_id, event_type, created_at)]
    )

def get_payloads():
    return client.execute('SELECT * FROM webhook.payloads')

def query_payloads(sender, recipient=None, status=None, start_date=None, end_date=None):
    query = "SELECT * FROM webhook.payloads WHERE sender = %(sender)s"
    params = {'sender': sender}

    if recipient:
        query += " AND recipient = %(recipient)s"
        params['recipient'] = recipient

    if status:
        query += " AND event_type = %(status)s"
        params['status'] = status

    if start_date:
        query += " AND created_at >= %(start_date)s"
        params['start_date'] = start_date

    if end_date:
        query += " AND created_at <= %(end_date)s"
        params['end_date'] = end_date

    return client.execute(query, params)

def get_all_payloads():
    return client.execute('SELECT * FROM webhook.payloads')

