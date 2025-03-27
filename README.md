# Sendbird Webhook Bot Responder

A FastAPI application that listens for Sendbird webhook events and automatically responds to new messages with a bot message.

## Overview

This application receives webhook events from Sendbird when a new message is sent in a group channel. When a valid user message is detected, the bot automatically responds with "Please wait while we connect you to a human agent".

The application includes safeguards to prevent infinite loops by checking the sender's identity before responding.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- HTTPX

## Installation

1. Clone this repository or download the source code.

2. Install required packages:

```bash
pip install fastapi uvicorn httpx
```

Or using the requirements.txt file:

```bash
pip install -r requirements.txt
```

3. Set the required environment variable:

```bash
export SENDBIRD_API_TOKEN="your_sendbird_api_token"
```

## Configuration

Edit the application code to set your Sendbird application ID and bot ID:

```python
# Sendbird application ID
SENDBIRD_APP_ID = "4DBB6182-C472-4943-A2D5-E8000F398ED1"
# Sendbird bot ID
SENDBIRD_BOT_ID = "f0a74288-8254-4415-9b3d-9ee90654a971"
```

## Running the Application

Run the application with:

```bash
python app.py
```

Or directly with uvicorn:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The application will start listening for webhook events on `http://your-server:8000/sbwebhook`.

## Configuring Sendbird Webhooks

1. Go to your Sendbird Dashboard
2. Navigate to Settings > Webhooks
3. Add a new webhook with the URL of your server: `http://your-server:8000/sbwebhook`
4. Select the "group_channel:message_send" event category
5. Save your webhook configuration

## Endpoints

- **POST /sbwebhook**: Receives webhook events from Sendbird
- **GET /latest_webhook**: Returns the most recent webhook payload (useful for debugging)

## Preventing Infinite Loops

The application includes checks to prevent the bot from responding to its own messages:

1. It checks if the sender's user_id matches the bot ID
2. It ignores messages from senders whose IDs start with the bot's ID prefix

## Logging

The application logs detailed information about received webhooks, bot message responses, and any errors encountered during processing. Check your console/logs for this information.

## Example Payload

The application is designed to handle payloads in this format:

```json
{
  "app_id": "4DBB6182-C472-4943-A2D5-E8000F398ED1",
  "category": "group_channel:message_send",
  "channel": {
    "channel_url": "sendbird_group_channel_251131019_12dfba9d993d651641f17f93e0bc8ee27da88db2",
    "name": "AI Chatbot Widget Channel",
    "custom_type": "SB_@I_@GENT"
  },
  "payload": {
    "message": "hi there",
    "message_id": 8007477985,
    "created_at": 1743049133959
  },
  "sender": {
    "user_id": "widget_c4858fe09cbc401c9a4d7ea5f0e62a01"
  }
}
```

## Troubleshooting

If you encounter issues:

1. Check that your environment variables are set correctly
2. Verify your Sendbird API token has the necessary permissions
3. Ensure your webhook URL is publicly accessible
4. Check the application logs for error messages

## License

[MIT License](LICENSE)