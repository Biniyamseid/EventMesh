
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
            payload String,
            created_at DateTime('UTC')
        ) ENGINE = MergeTree()
        ORDER BY created_at
    ''')

def insert_payload(payload):
    id = uuid4()
    created_at = datetime.now(timezone.utc)
    client.execute('INSERT INTO webhook.payloads (id, payload, created_at) VALUES', [(id, payload, created_at)])

def get_payloads():
    return client.execute('SELECT * FROM webhook.payloads')