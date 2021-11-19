import random
import requests
from requests.api import head
import time
from datetime import datetime, timedelta,timezone, date

class StibBot:
	def __init__(self, channel):
        	self.channel = channel

	def get_message_payload(self):
		ret_value = {"channel": self.channel,
			"blocks": [
			*self.get_metro_times()
			]
		}
		return ret_value

	def	get_text_from_metro_request(self, text) :
		text = text['points'][0]['passingTimes'] # get the main text of the response, we don't care about the crap that's before
		#init values
		ret_value = ""
		present_time = datetime.now() # UTC time
		present_time += timedelta(hours = 2)
		present_time = present_time.time()
		metro_time = ""
		FMT = '%H:%M:%S' # time format
		for i in text[:2] :
			ret_value += "Le métro destination " + i['destination']['fr'].title() + " "
			metro_time = i['expectedArrivalTime'].split("T")[1][0 : 8] # get the time and then substract the current time to it to get the time difference
			metro_time = datetime.strptime(metro_time, FMT).time()
			t_delta = datetime.combine(date.min, metro_time) - datetime.combine(date.min, present_time)
			print(t_delta.total_seconds())
			if(t_delta.total_seconds() < 0):
				ret_value += "arrivera dans 0 minutes :)" + "\n\n\n"
				continue 
			t_delta = str(t_delta)
			t_delta = t_delta.split(":")[1][0 : 2]
			if (t_delta[0] == '0') :
				t_delta = t_delta[1]
			ret_value += "arrivera dans " + t_delta + " minutes :)" + "\n\n\n"
		return ret_value
		
	def get_metro_times(self) :
		header = {"Accept" : "application/json", "Authorization" : "Bearer e936aa87b2245c38cc6bd8e3621575e5"}
		response1  = requests.get("https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/8022", headers=header)
		response2  = requests.get("https://opendata-api.stib-mivb.be/OperationMonitoring/4.0/PassingTimeByPoint/8021", headers=header)
		return {"type": "section", "text": {"type": "mrkdwn", "text": self.get_text_from_metro_request(response1.json())}},{"type": "section", "text": {"type": "mrkdwn", "text": self.get_text_from_metro_request(response2.json())}},
