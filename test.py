import requests
from datetime import datetime

# Define the query parameters
params = {
    'sender': 'example@sender.com',
    # 'recipient': 'example@recipient.com',
    # 'status': 'sent',
    # 'start_date': datetime(2024, 3, 1).isoformat(),
    # 'end_date': datetime(2024, 3, 9).isoformat(),
    'pagination_start': 0,
    'pagination_end': 10
}

# Make the GET request to the endpoint
response = requests.get('https://resend-webhook-fastapi.gj54va.easypanel.host/query?sender=onboarding@resend.dev', params=params)
# https://resend-webhook-fastapi.gj54va.easypanel.host/query?sender=onboarding@resend.dev

# Print the response JSON
print(response.json())