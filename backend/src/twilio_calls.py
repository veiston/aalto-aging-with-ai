"""
Twilio - Call Handling
Manages incoming/outgoing calls for elderly person

This module reads Twilio credentials from environment variables.
Do NOT commit real secrets. Use `.env` (local) and `.env.example` as a template.
"""
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def setup_twilio_client(account_sid: Optional[str] = None, auth_token: Optional[str] = None):
    """Initialize Twilio client using env vars if not provided.

    Returns a `twilio.rest.Client` instance or `None` if credentials or library missing.
    """
    sid = account_sid or os.environ.get("TWILIO_ACCOUNT_SID")
    token = auth_token or os.environ.get("TWILIO_AUTH_TOKEN")
    if not sid or not token:
        print("Twilio credentials not found in environment. Returning None.")
        return None

    try:
        from twilio.rest import Client
        return Client(sid, token)
    except Exception:
        print("Twilio library not available or failed to initialize. Install `twilio`.")
        return None


def receive_call(twilio_client, call_sid: str) -> dict:
    """
    Handle incoming call from elderly person.
    Fetch call details using Twilio API.
    """
    if not twilio_client:
        print("Twilio client not initialized.")
        return {}
    
    try:
        call = twilio_client.calls(call_sid).fetch()
        return {
            "from": call.from_,
            "to": call.to,
            "status": call.status,
            "sid": call.sid
        }
    except Exception as e:
        print(f"Failed to fetch call {call_sid}: {e}")
        return {}


def make_reminder_call(twilio_client, phone: str, from_number: Optional[str] = None) -> str:
    """Make outgoing reminder call with TwiML voice response.
    
    Args:
        twilio_client: Initialized Twilio Client
        phone: Recipient phone number (e.g., "+358401459556")
        from_number: Sender phone number (optional, uses env var or default)
    
    Returns:
        Call SID if successful, empty string otherwise
    """
    if not twilio_client:
        print("Twilio client not initialized. Cannot make call.")
        return ""
    
    try:
        call = twilio_client.calls.create(
            to=phone,
            from_=from_number if from_number else os.environ.get("TWILIO_FROM_NUMBER", "+15075568288"),
            url="http://demo.twilio.com/docs/voice.xml"
        )
        return call.sid
    except Exception as e:
        print(f"Failed to make reminder call: {e}")
        return ""


def transfer_to_family(twilio_client, call_sid: str, family_phone: str) -> bool:
    """Connect call to trusted family member.
    
    Args:
        twilio_client: Initialized Twilio Client
        call_sid: Active call SID to transfer
        family_phone: Target family member phone number
    
    Returns:
        True if transfer initiated, False otherwise
    """
    if not twilio_client:
        print("Twilio client not initialized.")
        return False
    
    try:
        twilio_client.calls(call_sid).update(
            twiml=f'<Response><Dial>{family_phone}</Dial></Response>'
        )
        return True
    except Exception as e:
        print(f"Failed to transfer call: {e}")
        return False


if __name__ == "__main__":
    # Test: call handling with real Twilio SDK
    client = setup_twilio_client()
    
    if client:
        # Make a test reminder call
        phone_number = "+358401459556"
        call_sid = make_reminder_call(client, phone_number)
        if call_sid:
            print(f"Reminder call sent. Call SID: {call_sid}")
            # Fetch and display call details
            call_info = receive_call(client, call_sid)
            print(f"Call info: {call_info}")
        else:
            print("Failed to make call.")
    else:
        print("Twilio client not initialized. Check .env credentials.")
