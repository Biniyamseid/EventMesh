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
from database.clickhouse import insert_payload, create_database, create_table,insert_h_data,insert_payload

app = Celery('tasks', broker='redis://default:8c3e85e077fd42b5264c@resend_webhook_redis_server:6379/0')
# app = Celery('tasks', broker='redis://localhost:6379/0')
# app = Celery('tasks', broker='redis://redis:6379/0')

create_database()
create_table()
insert_h_data.delay()
# insert_payload(    payload = {
#         "created_at": "2024-03-10T11:41:31.198Z",
#         "data": {
#             "created_at": "2024-03-10T11:41:30.456Z",
#             "email_id": "f3043bc9-f183-4435-a378-907562703ea9",
#             "from": "onboarding@resend.dev",
#             "subject": "Hello World",
#             "to": [
#                 "ethioartificialintelligence@gmail.com"
#             ]
#         },
#         "type": "email.delivered"
#     })



@app.task
def process_webhook_payload(payload):
    insert_payload(    payload = {
        "created_at": "2024-03-10T11:41:31.198Z",
        "data": {
            "created_at": "2024-03-10T11:41:30.456Z",
            "email_id": "f3043bc9-f183-4435-a378-907562703ea9",
            "from": "onboarding@resend.dev",
            "subject": "new 2",
            "to": [
                "on@shop.com"
            ]
        },
        "type": "email.delivered"
    })
    insert_payload(payload)