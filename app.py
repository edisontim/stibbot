import os
import logging
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from stibBot import StibBot

# Initialize a Flask app to host the events adapter
app = Flask(__name__)

# Create an events adapter and register it to an endpoint in the slack app for event ingestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

def get_times(channel):
	# Create a new CoinBot
	stib_bot = StibBot(channel)

	# Get the onboarding message payload
	message = stib_bot.get_message_payload()

	# Post the onboarding message in Slack
	slack_web_client.chat_postMessage(**message)

# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
	# Get the event data from the payload
	event = payload.get("event", {})

	# Get the text from the event that came through
	text = event.get("text")

	# Check and see if the activation phrase was in the text of the message.
	# If so, execute the code to flip a coin.
	if "!metro" in text.lower():
		# Since the activation phrase was met, get the channel ID that the event
		# was executed on
		channel_id = event.get("channel")

		# Execute the flip_coin function and send the results of
		# flipping a coin to the channel
		return get_times(channel_id)

if __name__ == "__main__":
	# Create the logging object
	logger = logging.getLogger()

	logger.setLevel(logging.DEBUG)
	
	logger.addHandler(logging.StreamHandler())

	app.run(host='0.0.0.0', port=3000)
