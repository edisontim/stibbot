import requests
from requests.api import head

header = {"Accept" : "application/json", "Authorization" : "Bearer 1a346c405a54d7f63ba0e7dbde24b96c"}
response  = requests.get("https://opendata-api.stib-mivb.be/NetworkDescription/1.0/PointByLine/5", headers=header)
print(response)

print(response.json())