


from celery import Celery
from database.clickhouse import insert_payload, create_database, create_table,insert_h_data,insert_payload
from celery import Celery
from celery.schedules import crontab
from resend_webhook.database.clickhouse import client
from datetime import datetime, timedelta, timezone
import logging
app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@resend_webhook_redis_server:6379/0',backend='db+sqlite:////app/results.db')

# app = Celery('tasks', broker='redis://redis:6379/0', backend='db+sqlite:////app/results.db')
# app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@resend_webhook_redis_server:6379/0',backend='db+sqlite:///results.sqlite3')
# app = Celery('tasks', broker='redis://localhost:6379/0')
# app = Celery('tasks', broker='redis://redis:6379/0')

create_database()
create_table()
# insert_h_data()
# insert_payload(    payload = {
#         "created_at": "2024-03-10T11:41:31.198Z",
#         "data": {
#             "created_at": "2024-03-10T11:41:30.456Z",
#             "email_id": "f3043bc9-f183-4435-a378-907562703ea9",
#             "from": "onboarding@resend.dev",
#             "subject": "Hello World",
#             "to": [
#                 "onshop@shop.com"
#             ]
#         },
#         "type": "email.delivered"
#     })



# @app.task
# def process_webhook_payload(payload):
#     # insert_payload(    payload = {
#     #     "created_at": "2024-03-10T11:41:31.198Z",
#     #     "data": {
#     #         "created_at": "2024-03-10T11:41:30.456Z",
#     #         "email_id": "f3043bc9-f183-4435-a378-907562703ea9",
#     #         "from": "onboarding@resend.dev",
#     #         "subject": "new 2",
#     #         "to": [
#     #             "on@shop.com"
#     #         ]
#     #     },
#     #     "type": "email.delivered"
#     # })
#     insert_payload(payload)


# @app.task
# def process_webhook_payload(payload):
#     try:
#         insert_payload(payload)
#         # logger.info("Payload processed and inserted into database.")
#     except Exception as e:
#         # logger.error(f"Failed to process payload: {e}")
#         raise


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

# @app.task
# def cleanup_database():
#     try:
#         # Calculate the Unix timestamp for 60 days ago
#         threshold = int((datetime.now(timezone.utc) - timedelta(days=60)).timestamp())
        
#         # Execute the query to delete old records
#         delete_query = "ALTER TABLE webhook.payloads DELETE WHERE created_at < %(threshold)s"
#         client.execute(delete_query, {'threshold': threshold})
        
#         logger.info("Database cleanup successful.")
#     except Exception as e:




# @app.task(bind=True)
# def process_webhook_payload(self, payload):
#     try:
#         insert_payload(payload)
#         return {"status": "success"}
#     except Exception as e:
#         self.update_state(state='FAILURE', meta=str(e))
#         raise


# from celery import Celery
# from database.clickhouse import insert_payload, create_database, create_table

# # app = Celery('tasks', broker='redis://localhost:6379/0')
# app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@resend_webhook_redis_server:6379/0')

# # Create database and table when Celery worker starts
# create_database()
# create_table()

# @app.task
# def process_webhook_payload(payload):
#     insert_payload(payload)



# _____________________________--Scheduling the Cleanup Task----
# app.conf.beat_schedule = {
#     'cleanup-database-every-60-days': {
#         'task': 'resend_webhook.celery_worker.cleanup_database',
#         'schedule': timedelta(days=60),
#     },
# }
