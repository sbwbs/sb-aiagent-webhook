from fastapi import FastAPI, Request, HTTPException
import uvicorn
import json
from datetime import datetime
import httpx
import os
import traceback  

app = FastAPI()

latest_payload = None

SENDBIRD_API_TOKEN = os.environ.get("SENDBIRD_API_TOKEN")
if not SENDBIRD_API_TOKEN:
    raise ValueError("SENDBIRD_API_TOKEN environment variable is not set")
else:
    print(f"SENDBIRD_API_TOKEN is set: {SENDBIRD_API_TOKEN[:5]}...")  # Partially log the token

# Sendbird application ID
SENDBIRD_APP_ID = "4DBB6182-C472-4943-A2D5-E8000F398ED1"
# Sendbird bot ID
SENDBIRD_BOT_ID = "f0a74288-8254-4415-9b3d-9ee90654a971"

async def send_bot_message(channel_url: str, message: str):
    """
    Send a message from the bot to the specified channel
    """
    url = f"https://api-{SENDBIRD_APP_ID}.sendbird.com/v3/bots/{SENDBIRD_BOT_ID}/send"
    headers = {
        "Api-Token": SENDBIRD_API_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "message": message,
        "channel_url": channel_url,
        "custom_type": "waiting_message"
    }
    
    print(f"Sending bot message to channel {channel_url}")
    
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        print(f"Bot message response status: {response.status_code}")
        if response.status_code != 200:
            print(f"Bot message error: {response.text}")
        response.raise_for_status()
        return response.json()

@app.post("/sbwebhook")
async def handle_sendbird_webhook(request: Request):
    global latest_payload
    try:
        payload = await request.json()
        print(f"Received webhook payload: {json.dumps(payload, indent=2)}")
        
        latest_payload = payload
        
        # Handle group_channel:message_send event
        if payload.get('category') == 'group_channel:message_send':
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Processing group_channel:message_send webhook...")
            
            # Extract channel_url from the payload
            channel_url = payload.get('channel', {}).get('channel_url')
            
            if channel_url:
                try:
                    # Send the waiting message from the bot
                    await send_bot_message(
                        channel_url, 
                        "Please wait while we connect you to a human agent"
                    )
                    print(f"Successfully sent bot message to channel {channel_url}")
                except Exception as e:
                    print(f"Error sending bot message: {str(e)}")
                    print(traceback.format_exc())
            else:
                print("Missing channel_url in the payload.")
        
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from request: {str(e)}")
        print(traceback.format_exc())
    except Exception as e:
        print(f"Unexpected error handling webhook: {str(e)}")
        print(traceback.format_exc())
    
    return {"status": "ok"}

@app.get("/latest_webhook")
async def get_latest_webhook():
    if latest_payload:
        return latest_payload
    else:
        return {"message": "No webhook payload received yet"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)