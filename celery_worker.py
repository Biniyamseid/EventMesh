from celery import Celery
from database.clickhouse import insert_payload, create_database, create_table,insert_h_data,insert_payload
from celery import Celery
from celery.schedules import crontab
from resend_webhook.database.clickhouse import client
from datetime import datetime, timedelta, timezone
import logging
app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@resend_webhook_redis_server:6379/0',backend='db+sqlite:////app/results.db')


create_database()
create_table()

logger = logging.getLogger(__name__)

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
def cleanup_database():
    try:
        # Calculate the Unix timestamp for 60 days ago
        threshold = int((datetime.now(timezone.utc) - timedelta(days=60)).timestamp())
        
        # Execute the query to delete old records
        delete_query = "ALTER TABLE webhook.payloads DELETE WHERE created_at < %(threshold)s"
        client.execute(delete_query, {'threshold': threshold})
        
        logger.info("Database cleanup successful.")
    except Exception as e:
        logger.error(f"Database cleanup failed: {e}")
        raise





# Then schedule for the cleanup_database task
app.conf.beat_schedule = {
    'cleanup-database-every-60-days': {
        'task': 'resend_webhook.celery_worker.cleanup_database',
        'schedule': timedelta(days=60),
    },
}

