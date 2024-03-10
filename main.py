
from datetime import datetime
import logging
from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from celery.exceptions import Retry
from celery_worker import process_webhook_payload
from fastapi import Query
from database.clickhouse import get_all_payloads, query_payloads
app = FastAPI()
logger = logging.getLogger(__name__)

from pydantic import BaseModel, Field
from typing import List

class EmailData(BaseModel):
    created_at: str
    email_id: str
    from_: str = Field(..., alias="from")
    subject: str
    to: List[str]

class WebhookPayload(BaseModel):
    created_at: str
    data: EmailData
    type: str



@app.get("/")
def read_root():
    return {"Hello": "welcome to resend webhook service"}

# def validate_payload(payload: WebhookPayload):
#     required_keys = ["created_at", "data", "type"]
#     data_keys = ["created_at", "email_id", "from_", "from","subject", "to"]

#     payload_dict = payload.model_dump()

#     if not all(key in payload_dict for key in required_keys):
#         return False

#     if not all(key in payload_dict["data"] for key in data_keys):
#         return False

#     return True

def validate_payload(payload: WebhookPayload):
    required_keys = ["created_at", "data", "type"]
    data_keys = ["created_at", "email_id", "from_","from", "subject", "to"]

    # payload_dict = payload.model_dump()
    payload_dict = payload

    missing_keys = [key for key in required_keys if key not in payload_dict]
    if missing_keys:
        return f"Missing required keys in payload: {', '.join(missing_keys)}"

    missing_data_keys = [key for key in data_keys if key not in payload_dict["data"]]
    if missing_data_keys:
        return f"Missing required keys in payload['data']: {', '.join(missing_data_keys)}"

    return True



@app.post("/webhook/resend")
async def receive_resend_notification(payload: WebhookPayload):
    """
    Receive a webhook payload and process it asynchronously.

    Args:
        payload (WebhookPayload): The webhook payload to process.

    Returns:
        dict: A dictionary with a single key "status" and value "received".
    """
    # t = "out of the block"
    try:
        # payload = await request.json()
        payload = payload.dict()
    except Exception:
        return {"status": "false", "detail": "Invalid JSON payload"}

    logger.info(f"WebhookPayload received: {payload}")
    try:
        if payload and validate_payload(payload):
            # t= "inside the block"
            process_webhook_payload.delay(payload)
            
        else:
            return {"status": "false", "detail": "Invalid payload"}
    except Exception as e:
        logger.error(f"Failed to process payload: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to process payload: {e,t}")
    return {"status": "received"}




@app.get("/query")
async def query_payloads_endpoint(
    sender: str,
    recipient: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)
):
    results = query_payloads(sender, recipient, status, start_date, end_date)
    return {"payloads": results}

@app.get("/query/all")
async def query_all_payloads_endpoint():
    results = get_all_payloads()
    return {"payloads": results}
