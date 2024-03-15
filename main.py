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
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.status import HTTP_401_UNAUTHORIZED
import secrets


security = HTTPBasic()
app = FastAPI()
logger = logging.getLogger(__name__)



@app.get("/")
def read_root():
    return {"Hello": "World"}


def validate_payload(payload):
    """
    Validates the structure and content of a webhook payload.

    This function checks if the payload is a dictionary, contains the required top-level keys,
    and if the 'data' key is a dictionary with the required data keys.

    Args:
        payload (dict): The webhook payload to validate.

    Returns:
        bool: True if the payload is valid, False otherwise.

    Required top-level keys:
        - 'created_at': The timestamp when the event was created.
        - 'data': A dictionary containing the event data.
        - 'type': The type of the event.

    Required data keys:
        - 'created_at': The timestamp when the email was created.
        - 'email_id': The unique identifier for the email.
        - 'from': The email address of the sender.
        - 'subject': The subject of the email.
        - 'to': The recipient(s) of the email.
    """
    required_keys = ["created_at", "data", "type"]
    data_keys = ["created_at", "email_id", "from", "subject", "to"]

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
            insert_payload(payload)
            task = process_webhook_payload.delay(payload)
            return {"status": "received"}

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





def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "secret")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/query/all")
async def query_all_payloads_endpoint(username: str = Depends(get_current_username)):
    results = get_all_payloads()
    return {"payloads": results}




