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


from celery import Celery
from database.clickhouse import insert_payload, create_database, create_table,insert_h_data

app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@resend_webhook_redis_server:6379/0')
# app = Celery('tasks', broker='redis://localhost:6379/0')
# app = Celery('tasks', broker='redis://redis:6379/0')

create_database()
create_table()
insert_h_data()

@app.task
def process_webhook_payload(payload):
    insert_payload(payload)