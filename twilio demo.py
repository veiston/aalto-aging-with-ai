# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "ACb7ec9f665735dedf209df4a70f721ca8"
auth_token = "477213dde4d6baa062d6615c3fe70e4f"
client = Client(account_sid, auth_token)

call = client.calls.create(
  url="http://demo.twilio.com/docs/voice.xml",
  to="+358401459556",
  from_="+15075568288"
)

print(call.sid)