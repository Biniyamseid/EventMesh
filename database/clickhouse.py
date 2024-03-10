
from clickhouse_driver import Client
from uuid import uuid4
from datetime import datetime, timezone

# client = Client('localhost')
client = Client('resend-webhook-clickhouse.gj54va.easypanel.host')
# -----------------------------------
def create_database():
    client.execute('CREATE DATABASE IF NOT EXISTS webhook')

def create_table():
    client.execute('''
        CREATE TABLE IF NOT EXISTS webhook.payloads (
            id UUID,
            sender String,
            recipient String,
            subject String,
            html String,
            created_at DateTime('UTC')
        ) ENGINE = MergeTree()
        ORDER BY created_at
    ''')

def insert_payload(payload):
    # Parse the payload
    sender = payload.get("from")
    recipient = payload.get("to")
    subject = payload.get("subject")
    html = payload.get("html")

    # Check if sender is present
    if not sender:
        raise ValueError("Payload must include a 'from' value")

    # Generate id and created_at values
    id = uuid4()
    created_at = datetime.now(timezone.utc)

    # Insert into database
    client.execute(
        'INSERT INTO webhook.payloads (id, sender, recipient, subject, html, created_at) VALUES',
        [(id, sender, recipient, subject, html, created_at)]
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
        query += " AND status = %(status)s"
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