
from clickhouse_driver import Client
from uuid import uuid4
from datetime import datetime, timezone

# client = Client('localhost')
client = Client('clickhouse')
def create_database():
    client.execute('CREATE DATABASE IF NOT EXISTS webhook')



def create_table():
    client.execute('''
        CREATE TABLE IF NOT EXISTS webhook.payloads (
            id UUID,
            sender String,
            recipient String,
            status String,
            payload String,
            created_at DateTime('UTC')
        ) ENGINE = MergeTree()
        ORDER BY created_at
    ''')

# ---------------------------------------------------------------
# def create_database():
#     client.execute('DROP DATABASE IF EXISTS webhook')
#     client.execute('CREATE DATABASE webhook')

# def create_table():
#     client.execute('DROP TABLE IF EXISTS webhook.payloads')
#     client.execute('''
#         CREATE TABLE webhook.payloads (
#             id UUID,
#             sender String,
#             recipient String,
#             status String,
#             payload String,
#             created_at DateTime('UTC')
#         ) ENGINE = MergeTree()
#         ORDER BY created_at
#     ''')

# ------------------------------------------

# def create_table():
#     client.execute('''
#         CREATE TABLE IF NOT EXISTS webhook.payloads (
#             id UUID,
#             payload String,
#             created_at DateTime('UTC')
#         ) ENGINE = MergeTree()
#         ORDER BY created_at
#     ''')
    
def insert_payload(payload):
    id = uuid4()
    created_at = datetime.now(timezone.utc)
    client.execute('INSERT INTO webhook.payloads (id, sender, recipient, status, payload, created_at) VALUES', [(id, payload['sender'], payload['recipient'], payload['status'], payload['payload'], created_at)])

# def insert_payload(payload):
#     id = uuid4()
#     created_at = datetime.now(timezone.utc)
#     client.execute('INSERT INTO webhook.payloads (id, payload, created_at) VALUES', [(id, payload, created_at)])

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