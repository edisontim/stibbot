from slack import WebClient
from stibBot import StibBot
import os
import ssl #SECURITY CONCERNS HERE ? 

ssl._create_default_https_context = ssl._create_unverified_context


token=os.environ.get("SLACK_TOKEN")
print(token)
# Create a slack client
slack_web_client = WebClient(os.environ.get("SLACK_TOKEN"))

# Get a new CoinBot
stib_bot = StibBot("#général")

# Get the onboarding message payload
message = stib_bot.get_message_payload()

# Post the onboarding message in Slack
slack_web_client.chat_postMessage(**message)
