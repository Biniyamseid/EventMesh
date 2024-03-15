from fastapi import FastAPI
from celery.result import AsyncResult
from celery_worker import fetch_all_payloads_task, process_webhook_payload, app as celery_app
from datetime import datetime
import logging
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from celery.exceptions import Retry
from celery_worker import process_webhook_payload
from fastapi import Query
from database.clickhouse import get_all_payloads, query_payloads
from database.clickhouse import insert_payload, create_database, create_table,insert_h_data,insert_payload
app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"Hello": "World"}


def validate_payload(payload):
    required_keys = ["created_at", "data", "type"]
    data_keys = ["created_at", "email_id", "from", "subject", "to"]
    payload = payload
    if not isinstance(payload, dict):
        return False

    if not all(key in payload for key in required_keys):
        return False

    if not isinstance(payload["data"], dict):
        return False

    if not all(key in payload["data"] for key in data_keys):
        return False

    return True



@app.post("/webhook/resend")
async def receive_resend_notification(request: Request):
    """
    Receive a webhook payload and process it asynchronously.

    Args:
        payload (WebhookPayload): The webhook payload to process.

    Returns:
        dict: A dictionary with a single key "status" and value "received".
    """
    try:
        payload = await request.json()
        logger.info(f"WebhookPayload received: {payload}")
    except Exception as e:
        return {"status": "false", "detail": "Invalid JSON payload"}
    try:
        if payload and validate_payload(payload):
            # insert_payload(payload)
            task = process_webhook_payload.delay(payload)
            return {"status": "received", "task_id": task.id}
            # return {"status": "received"}

        else:
            return {"status": "false"}
    except Exception as e:
        logger.error(f"Failed to process payload: {e}")
        raise HTTPException(status_code=500, detail= f"Failed to process payload{e}")
    return {"status": "done"}




@app.get("/query")
async def query_payloads_endpoint(
    sender: str,
    recipient: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    pagination_start: Optional[int] = Query(0),
    pagination_end: Optional[int] = Query(15)
):
    results = query_payloads(sender, recipient, status, start_date, end_date, pagination_start, pagination_end)
    return {"payloads": results}





# @app.get("/query/all")
# async def query_all_payloads_endpoint():
#     results = get_all_payloads()
#     return {"payloads": results}

from celery.result import AsyncResult

# @app.get("/query/all")
# async def query_all_payloads_endpoint():
#     # Dispatch the task
#     task = fetch_all_payloads_task.delay()
    
#     # Wait for the task to finish and get the result
#     # Note: In a production environment, consider adding a timeout or handling long-running tasks differently
#     result = AsyncResult(task.id).get()
    
#     return {"payloads": result}

from celery.result import AsyncResult
from fastapi import HTTPException

@app.get("/query/all")
async def query_all_payloads_endpoint():
    task = fetch_all_payloads_task.delay()
    
    try:
        # Wait for the task to finish with a timeout (e.g., 10 seconds)
        result = AsyncResult(task.id).get(timeout=10)
    except TimeoutError:
        raise HTTPException(status_code=504, detail="Request timed out")
    except Exception as e:
        # Handle other exceptions, such as task execution errors
        raise HTTPException(status_code=500, detail=str(e))
    
    return {"payloads": result}















