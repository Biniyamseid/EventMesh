from datetime import datetime, timedelta, timezone
from datetime import datetime
from celery import Celery
from database.clickhouse import insert_payload, create_database, create_table,insert_h_data,insert_payload
# app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@resend_webhook_redis_server:6379/0',backend='db+sqlite:////app/results.db')
app = Celery('tasks', broker='redis://redis:6379/0', backend='db+sqlite:////app/results.db')
app.conf.broker_connection_retry_on_startup = True
from database.clickhouse import client
from celery.schedules import crontab
create_database()
create_table()

@app.task(bind=True)
def process_webhook_payload(self, payload):
    try:
        self.update_state(state='STARTED')
        insert_payload(payload)
        self.update_state(state='SUCCESS')
        return {"status": "success"}
    except Exception as e:
        self.update_state(state='FAILURE', meta=str(e))
        raise


@app.task
def cleanup_old_records():
    threshold = int((datetime.now(datetime.timezone.utc) - timedelta(days=60)).timestamp())
    delete_query = "ALTER TABLE webhook.payloads DELETE WHERE created_at < %(threshold)s"
    client.execute(delete_query, {'threshold': threshold})


app.conf.beat_schedule = {
    'cleanup-every-60-days': {
        'task': 'resend_webhook.celery_worker.cleanup_old_records',
        'schedule': timedelta(days=60),
    },
}
