from datetime import datetime, timedelta, timezone
from datetime import datetime
from celery import Celery
from database.clickhouse import get_all_payloads, insert_payload, create_database, create_table,insert_h_data,insert_payload
app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@resend_webhook_redis_server:6379/0',backend='db+sqlite:////app/results.db')
# app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@redis:6379/0', backend='db+sqlite:////app/results.db')
# app = Celery('tasks', broker='redis://redis:6379/0', backend='db+sqlite:////app/results.db')
app.conf.broker_connection_retry_on_startup = True
from database.clickhouse import client
from celery.schedules import crontab

import time

MAX_RETRIES = 5
RETRY_DELAY = 10  # seconds

def create_database_with_retry():
    for attempt in range(MAX_RETRIES):
        try:
            create_database()
            break  # Success, exit the loop
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)  # Wait before retrying
            else:
                raise  # Re-raise the exception if max retries reached

def create_table_with_retry():
    for attempt in range(MAX_RETRIES):
        try:
            create_table()
            break  # Success, exit the loop
        except Exception as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)  # Wait before retrying
            else:
                raise  # Re-raise the exception if max retries reached


create_database_with_retry()
create_table_with_retry()

@app.task
def fetch_all_payloads_task():
    try:
        results = get_all_payloads()
        return results
    except Exception as e:
        # Log the error or handle it as needed
        raise e



@app.task(bind=True, max_retries=10, default_retry_delay=19)  # Configure retries here
def process_webhook_payload(self, payload):
    try:
        self.update_state(state='STARTED')
        insert_payload(payload)  # Attempt to insert the payload
        self.update_state(state='SUCCESS')
        return {"status": "success"}
    except Exception as e:
        self.update_state(state='FAILURE', meta=str(e))
        try:
            # Retry the task
            self.retry(exc=e)
        except Exception as e:
            # Handle the case when max retries have been exceeded
            raise e


@app.task
def cleanup_old_records():
    threshold = int((datetime.now(datetime.timezone.utc) - timedelta(days=60)).timestamp())
    delete_query = "ALTER TABLE webhook.payloads DELETE WHERE created_at < %(threshold)s"
    client.execute(delete_query, {'threshold': threshold})


app.conf.update(
    task_time_limit=30,
    worker_concurrency=4,
    task_annotations={'my_task': {'rate_limit': '10/m'}},
    worker_prefetch_multiplier=1,
    broker_transport_options={'visibility_timeout': 3600},
    event_queue_expires=3600
)

app.conf.beat_schedule = {
    'cleanup-every-60-days': {
        'task': 'resend_webhook.celery_worker.cleanup_old_records',
        'schedule': timedelta(days=60),
    },
}
