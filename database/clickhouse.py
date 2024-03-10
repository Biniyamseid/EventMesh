
# from clickhouse_driver import Client
# from uuid import uuid4
# from datetime import datetime, timezone

# # client = Client('localhost')
# client = Client('resend_webhook_clickhouse')
# # -----------------------------------




# from clickhouse_driver import Client, errors
# from uuid import uuid4
# from datetime import datetime, timezone
# import logging

# logger = logging.getLogger(__name__)

# def create_database():
#     try:
#         logger.info("Creating database...")
#         client.execute('CREATE DATABASE IF NOT EXISTS webhook')
#         logger.info("Database created successfully.")
#     except errors.Error as e:
#         logger.error(f"Failed to create database: {e}")
#         raise

# def create_table():
#     try:
#         logger.info("Creating table...")
#         client.execute('''
#             CREATE TABLE IF NOT EXISTS webhook.payloads (
#                 id UUID,
#                 sender String,
#                 recipient String,
#                 subject String,
#                 email_id String,
#                 event_type String,
#                 created_at DateTime('UTC')
#             ) ENGINE = MergeTree()
#             ORDER BY created_at
#         ''')
#         logger.info("Table created successfully.")
#     except errors.Error as e:
#         logger.error(f"Failed to create table: {e}")
#         raise

# def insert_payload(payload):
#     sender = payload["data"].get("from")
#     recipient = payload["data"].get("to")[0] if payload["data"].get("to") else None
#     subject = payload["data"].get("subject")
#     email_id = payload["data"].get("email_id")
#     event_type = payload.get("type")

#     if not sender:
#         raise ValueError("Payload must include a 'from' value")

#     id = uuid4()
#     created_at = datetime.fromisoformat(payload["created_at"].replace("Z", "+00:00"))

#     try:
#         logger.info("Inserting payload...")
#         client.execute(
#             'INSERT INTO webhook.payloads (id, sender, recipient, subject, email_id, event_type, created_at) VALUES',
#             [(id, sender, recipient, subject, email_id, event_type, created_at)]
#         )
#         logger.info("Payload inserted successfully.")
#     except errors.Error as e:
#         logger.error(f"Failed to insert payload: {e}")
#         raise

# def get_payloads():
#     try:
#         logger.info("Getting payloads...")
#         result = client.execute('SELECT * FROM webhook.payloads')
#         logger.info("Payloads retrieved successfully.")
#         return result
#     except errors.Error as e:
#         logger.error(f"Failed to get payloads: {e}")
#         raise

# def query_payloads(sender, recipient=None, status=None, start_date=None, end_date=None):
#     query = "SELECT * FROM webhook.payloads WHERE sender = %(sender)s"
#     params = {'sender': sender}

#     if recipient:
#         query += " AND recipient = %(recipient)s"
#         params['recipient'] = recipient

#     if status:
#         query += " AND event_type = %(status)s"
#         params['status'] = status

#     if start_date:
#         query += " AND created_at >= %(start_date)s"
#         params['start_date'] = start_date

#     if end_date:
#         query += " AND created_at <= %(end_date)s"
#         params['end_date'] = end_date

#     try:
#         logger.info("Querying payloads...")
#         result = client.execute(query, params)
#         logger.info("Payloads queried successfully.")
#         return result
#     except errors.Error as e:
#         logger.error(f"Failed to query payloads: {e}")
#         raise

# def get_all_payloads():
#     try:
#         logger.info("Getting all payloads...")
#         result = client.execute('SELECT * FROM webhook.payloads')
#         logger.info("All payloads retrieved successfully.")
#         return result
#     except errors.Error as e:
#         logger.error(f"Failed to get all payloads: {e}")
#         raise





# 2--------------------------------------



# from clickhouse_driver import Client, errors
# from uuid import uuid4
# from datetime import datetime, timezone
# import logging

# logger = logging.getLogger(__name__)
# client = Client('resend_webhook_clickhouse')



# def test_database_connection():
#     try:
#         result = client.execute('SELECT 1')
#         logger.info(f"Database connection test result: {result}")
#     except errors.Error as e:
#         logger.error(f"Failed to connect to database: {e}")
#         return {"status": "false", "detail": "database connection failed"}
#         # raise
        
# test_database_connection()

# def create_database():
#     try:
#         logger.info("Creating database...")
#         client.execute('CREATE DATABASE IF NOT EXISTS webhook')
#         logger.info("Database created successfully.")
#     except errors.Error as e:
#         logger.error(f"Failed to create database: {e}")
#         raise

# def create_table():
#     try:
#         logger.info("Creating table...")
#         client.execute('''
#             CREATE TABLE IF NOT EXISTS webhook.payloads (
#                 id UUID,
#                 sender String,
#                 recipient String,
#                 subject String,
#                 email_id String,
#                 event_type String,
#                 created_at DateTime('UTC')
#             ) ENGINE = MergeTree()
#             ORDER BY created_at
#         ''')
#         logger.info("Table created successfully.")
#     except errors.Error as e:
#         logger.error(f"Failed to create table: {e}")
#         raise

# def insert_payload(payload):
#     sender = payload["data"].get("from")
#     recipient = payload["data"].get("to")[0] if payload["data"].get("to") else None
#     subject = payload["data"].get("subject")
#     email_id = payload["data"].get("email_id")
#     event_type = payload.get("type")

#     if not sender:
#         raise ValueError("Payload must include a 'from' value")

#     id = uuid4()
#     created_at = datetime.fromisoformat(payload["created_at"].replace("Z", "+00:00"))

#     try:
#         logger.info("Inserting payload...")
#         client.execute(
#             'INSERT INTO webhook.payloads (id, sender, recipient, subject, email_id, event_type, created_at) VALUES',
#             [(id, sender, recipient, subject, email_id, event_type, created_at)]
#         )
#         logger.info("Payload inserted successfully.")
#     except errors.Error as e:
#         logger.error(f"Failed to insert payload: {e}")
#         raise

# def get_payloads():
#     try:
#         logger.info("Getting payloads...")
#         result = client.execute('SELECT * FROM webhook.payloads')
#         logger.info("Payloads retrieved successfully.")
#         return result
#     except errors.Error as e:
#         logger.error(f"Failed to get payloads: {e}")
#         raise

# def query_payloads(sender, recipient=None, status=None, start_date=None, end_date=None):
#     query = "SELECT * FROM webhook.payloads WHERE sender = %(sender)s"
#     params = {'sender': sender}

#     if recipient:
#         query += " AND recipient = %(recipient)s"
#         params['recipient'] = recipient

#     if status:
#         query += " AND event_type = %(status)s"
#         params['status'] = status

#     if start_date:
#         query += " AND created_at >= %(start_date)s"
#         params['start_date'] = start_date

#     if end_date:
#         query += " AND created_at <= %(end_date)s"
#         params['end_date'] = end_date

#     try:
#         logger.info("Querying payloads...")
#         result = client.execute(query, params)
#         logger.info("Payloads queried successfully.")
#         return result
#     except errors.Error as e:
#         logger.error(f"Failed to query payloads: {e}")
#         raise

# def get_all_payloads():
#     try:
#         logger.info("Getting all payloads...")
#         result = client.execute('SELECT * FROM webhook.payloads')
#         logger.info("All payloads retrieved successfully.")
#         return result
#     except errors.Error as e:
#         logger.error(f"Failed to get all payloads: {e}")
#         raise



# ----------------3------------------

from clickhouse_driver import Client
from uuid import uuid4
from datetime import datetime, timezone

# client = Client('localhost')
client = Client('resend_webhook_clickhouse')
# client = Client('clickhouse')
# client = Client('clickhouse')

# -----------------------------------



# def create_database():
#     client.execute('DROP DATABASE IF EXISTS webhook')
#     client.execute('CREATE DATABASE IF NOT EXISTS webhook')

# def create_table():
#     # client.execute('DROP TABLE IF EXISTS webhook.payloads')
#     client.execute('''
#         CREATE TABLE IF NOT EXISTS webhook.payloads (
#             id UUID,
#             sender String,
#             recipient String,
#             subject String,
#             email_id String,
#             event_type String,
#             created_at DateTime('UTC')
#         ) ENGINE = MergeTree()
#         ORDER BY created_at
#     ''')

# def insert_payload(payload):
#     # Parse the payload
#     sender = payload["data"].get("from")
#     recipient = payload["data"].get("to")[0] if payload["data"].get("to") else None
#     subject = payload["data"].get("subject")
#     email_id = payload["data"].get("email_id")
#     event_type = payload.get("type")

#     # Check if sender is present
#     if not sender:
#         raise ValueError("Payload must include a 'from' value")

#     # Generate id and created_at values
#     id = uuid4()
#     created_at = datetime.fromisoformat(payload["created_at"].replace("Z", "+00:00"))

#     # Insert into database
#     client.execute(
#         'INSERT INTO webhook.payloads (id, sender, recipient, subject, email_id, event_type, created_at) VALUES',
#         [(id, sender, recipient, subject, email_id, event_type, created_at)]
#     )

# def get_payloads():
#     return client.execute('SELECT * FROM webhook.payloads')

# def query_payloads(sender, recipient=None, status=None, start_date=None, end_date=None):
#     query = "SELECT * FROM webhook.payloads WHERE sender = %(sender)s"
#     params = {'sender': sender}

#     if recipient:
#         query += " AND recipient = %(recipient)s"
#         params['recipient'] = recipient

#     if status:
#         query += " AND event_type = %(status)s"
#         params['status'] = status

#     if start_date:
#         query += " AND created_at >= %(start_date)s"
#         params['start_date'] = start_date

#     if end_date:
#         query += " AND created_at <= %(end_date)s"
#         params['end_date'] = end_date

#     return client.execute(query, params)

# def get_all_payloads():
#     return client.execute('SELECT * FROM webhook.payloads')


# ------------------------------------------------------------
from clickhouse_driver import Client, errors
from uuid import uuid4
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)
# client = Client('clickhouse')
client = Client('resend_webhook_clickhouse')

def create_database():
    try:
        logger.info("Creating database...")
        client.execute('CREATE DATABASE IF NOT EXISTS webhook')
        logger.info("Database created successfully.")
    except errors.Error as e:
        logger.error(f"Failed to create database: {e}")
        raise

def create_table():
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
                created_at DateTime('UTC')
            ) ENGINE = MergeTree()
            ORDER BY created_at
        ''')
        logger.info("Table created successfully.")
    except errors.Error as e:
        logger.error(f"Failed to create table: {e}")
        raise

def insert_payload(payload):
    sender = payload["data"].get("from")
    recipient = payload["data"].get("to")[0] if payload["data"].get("to") else None
    subject = payload["data"].get("subject")
    email_id = payload["data"].get("email_id")
    event_type = payload.get("type")

    if not sender:
        raise ValueError("Payload must include a 'from' value")

    id = uuid4()
    created_at = datetime.fromisoformat(payload["created_at"].replace("Z", "+00:00"))

    try:
        logger.info("Inserting payload...")
        client.execute(
            'INSERT INTO webhook.payloads (id, sender, recipient, subject, email_id, event_type, created_at) VALUES',
            [(id, sender, recipient, subject, email_id, event_type, created_at)]
        )
        logger.info("Payload inserted successfully.")
    except errors.Error as e:
        logger.error(f"Failed to insert payload: {e}")
        raise

def get_payloads():
    try:
        logger.info("Getting payloads...")
        result = client.execute('SELECT * FROM webhook.payloads')
        logger.info("Payloads retrieved successfully.")
        return result
    except errors.Error as e:
        logger.error(f"Failed to get payloads: {e}")
        raise

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

    try:
        logger.info("Querying payloads...")
        result = client.execute(query, params)
        logger.info("Payloads queried successfully.")
        return result
    except errors.Error as e:
        logger.error(f"Failed to query payloads: {e}")
        raise

def get_all_payloads():
    try:
        logger.info("Getting all payloads...")
        result = client.execute('SELECT * FROM webhook.payloads')
        logger.info("All payloads retrieved successfully.")
        return result
    except errors.Error as e:
        logger.error(f"Failed to get all payloads: {e}")
        raise