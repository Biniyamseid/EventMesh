import logging
from fastapi import FastAPI, Request, HTTPException
from celery.exceptions import Retry
from celery_worker import process_webhook_payload

app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/webhook/resend")
async def receive_resend_notification(request: Request):
    """
    Receive a webhook payload and process it asynchronously.

    Args:
        payload (WebhookPayload): The webhook payload to process.

    Returns:
        dict: A dictionary with a single key "status" and value "received".
    """
    payload = await request.json()
    try:
        process_webhook_payload.delay(payload)
    except Exception as e:
        logger.error(f"Failed to process payload: {e}")
        raise HTTPException(status_code=500, detail="Failed to process payload")
    return {"status": "received"}
