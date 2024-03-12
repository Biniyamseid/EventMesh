import resend

# resend.api_key = "re_VzippoMR_NP1rCWL44UVeAnbAQA4mXxQo"
# https://resend-webhook-fastapi.gj54va.easypanel.host/webhook/resend
resend.api_key = "re_8ngxrF3m_3yBQBRVrbQsGDVkcBUWbjdgy"

r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": "info@n8n.shop",
  "subject": "New Message 4",
  "html": "<p>Congrats on sending your <strong>first email hello</strong>!</p>"
})

print(r)