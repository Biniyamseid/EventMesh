import resend

resend.api_key = "re_8ngxrF3m_3yBQBRVrbQsGDVkcBUWbjdgy"

r = resend.Emails.send({
  "from": "onboarding@resend.dev",
  "to": "info@n8n.shop",
  "subject": "New Message 4",
  "html": "<p>Congrats on sending your <strong>first email hello</strong>!</p>"
})

print(r)