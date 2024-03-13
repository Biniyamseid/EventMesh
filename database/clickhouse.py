from clickhouse_driver import Client, errors
from uuid import uuid4
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
# client = Client('clickhouse')
client = Client('resend_webhook_clickhouse')

def create_database():
    try:
        # client.execute('DROP DATABASE IF EXISTS webhook')
        logger.info("Creating database...")
        client.execute('CREATE DATABASE IF NOT EXISTS webhook')
        logger.info("Database created successfully.")
    except errors.Error as e:
        logger.error(f"Failed to create database: {e}")
        raise

    "update the database row,date"

def create_table():
    """
     you should consider adding indexes on the sender and event_type columns to improve the performance of the queries.
     This can be done by modifying the CREATE TABLE statement to include indexes:
    
    """
    try:
        logger.info("Creating table...")
        client.execute('''
    CREATE TABLE IF NOT EXISTS webhook.payloads (
        id UUID,
        sender String,
        recipient String,
        subject String,
        email_id String,
        event_type String,
        created_at DateTime('UTC'),
        INDEX sender_idx (sender) TYPE bloom_filter() GRANULARITY 1,
        INDEX event_type_idx (event_type) TYPE bloom_filter() GRANULARITY 1
    ) ENGINE = MergeTree()
    ORDER BY (sender, event_type, created_at)
    SETTINGS index_granularity = 8192
''')
        logger.info("Table created successfully.")
    except errors.Error as e:
        logger.info(f"Failed to create table: {e}")
        raise

def insert_payload(payload):
    id = str(uuid4())
    sender = payload['data']['from']
    recipient = payload['data']['to'][0]
    subject = payload['data']['subject']
    email_id = payload['data']['email_id']
    event_type = payload['type']
    created_at = datetime.strptime(payload['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)

    try:
        client.execute(
            'INSERT INTO webhook.payloads (id, sender, recipient, subject, email_id, event_type, created_at) VALUES',
            [(id, sender, recipient, subject, email_id, event_type, created_at)]
        )
        logger.info("Hardcoded data inserted successfully.")
    except errors.Error as e:
        logger.info(f"Failed to insert  data: {e}")
        raise
    

def insert_h_data():
    """
    this function inserts hardcoded data into the payloads table for testing purposes.
    """
    payload = {
        "created_at": "2024-03-10T11:41:31.198Z",
        "data": {
            "created_at": "2024-03-10T11:41:30.456Z",
            "email_id": "f3043bc9-f183-4435-a378-907562703ea9",
            "from": "onboarding@resend.dev",
            "subject": "data",
            "to": [
                "example@example.com"
            ]
        },
        "type": "email.delivered"
    }

    id = str(uuid4())
    sender = payload['data']['from']
    recipient = payload['data']['to'][0]
    subject = payload['data']['subject']
    email_id = payload['data']['email_id']
    event_type = payload['type']
    created_at = datetime.strptime(payload['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=timezone.utc)

    try:
        client.execute(
            'INSERT INTO webhook.payloads (id, sender, recipient, subject, email_id, event_type, created_at) VALUES',
            [(id, sender, recipient, subject, email_id, event_type, created_at)]
        )
        logger.info("Hardcoded data inserted successfully.")
    except errors.Error as e:
        logger.info(f"Failed to insert  data: {e}")
        raise



def get_payloads():
    try:
        logger.info("Getting payloads...")
        result = client.execute('SELECT * FROM webhook.payloads')
        logger.info("Payloads retrieved successfully.")
        return result
    except errors.Error as e:
        logger.info(f"Failed to get payloads: {e}")
        raise

# _____________________2
# ... (other imports and functions)

def query_payloads(sender, recipient=None, status=None, start_date=None, end_date=None, pagination_start=0, pagination_end=15):
    query = "SELECT * FROM webhook.payloads WHERE sender = %(sender)s"
    params = {'sender': sender}

    if recipient:
        query += " AND recipient = %(recipient)s"
        params['recipient'] = recipient

    if status:
        query += " AND event_type = %(status)s"
        params['status'] = status

    if start_date:
        # Assuming start_date is already a datetime object
        start_timestamp = int(start_date.timestamp())
        query += " AND created_at >= toDateTime(%(start_timestamp)s)"
        params['start_timestamp'] = start_timestamp

    if end_date:
        # Assuming end_date is already a datetime object
        end_timestamp = int(end_date.timestamp())
        query += " AND created_at <= toDateTime(%(end_timestamp)s)"
        params['end_timestamp'] = end_timestamp

    # Add ORDER BY and LIMIT with OFFSET for pagination
    query += " ORDER BY created_at DESC LIMIT %(pagination_start)s, %(pagination_end)s"
    params['pagination_start'] = pagination_start
    params['pagination_end'] = pagination_end - pagination_start  # Adjust because LIMIT takes the count, not the end index

    try:
        logger.info("Querying payloads...")
        result = client.execute(query, params)
        logger.info("Payloads queried successfully.")
        return result
    except errors.Error as e:
        logger.info(f"Failed to query payloads: {e}")
        raise



def get_all_payloads():
    try:
        logger.info("Getting all payloads...")
        result = client.execute('SELECT * FROM webhook.payloads')
        logger.info("All payloads retrieved successfully.")
        return result
    except errors.Error as e:
        logger.info(f"Failed to get all payloads: {e}")
        raise