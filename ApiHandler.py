from util import util
from uber_rides.session import Session
from uber_rides.client import UberRidesClient
import random, string

session = Session(server_token="pDZC0A3CV1bylgwrZ4Sw0098w5kFxPJS82YDN4KB")
client = UberRidesClient(session)

class ApiHandler:

	@staticmethod
	def getSuggestions(inputString):
		response = util.hitApi("https://maps.googleapis.com/maps/api/place/autocomplete/json?input=IIT&types=establishment&location=28.644800,77.216721&radius=50000&strictbounds&key=AIzaSyCJ4g5IXIkFKgR9Ck2Z8Aa1tPoi90CkNUY")
		if(response['status'] == "OK"):
			returnList = []
			for i in response['predictions']:
				returnList.append(i['description'])
			return returnList
		else:
			return []

	@staticmethod
	def getCoordinates(stop):
		stop = stop + " delhi"
		response = util.hitApi("https://maps.googleapis.com/maps/api/geocode/json?address=" + stop + "&key=AIzaSyBpMr3IX_arUxqVsksiKBCUwDMnOO1moRI")
		if(response['status'] == "OK"):
			return {
				"lat": response['results'][0]['geometry']['location']['lat'],
				"lng": response['results'][0]['geometry']['location']['lng']
			}
		else:
			return {
				"lat": -1,
				"lng": -1
			}

	@staticmethod
	def bestRoute(source, destination):
		response = util.hitApi("https://maps.googleapis.com/maps/api/directions/json?origin=" + source + "&destination=" + destination + "&key=AIzaSyBpMr3IX_arUxqVsksiKBCUwDMnOO1moRI")
		if(response['status'] == "OK"):
			timeTaken = response['routes'][0]['legs'][0]['duration']['text']
			distance = response['routes'][0]['legs'][0]['distance']['text']
			return {
				"time": timeTaken,
				"distance": distance
			}
	@staticmethod
	def uberGoPrice(startLat, startLong, endLat, endLong, startName, endName):
		# First get uber development dashboard registered.
		# response = util.hitApi('https://api.uber.com/v1.2/products?latitude=37.7759792&longitude=-122.41823')
		# Done that above!
		response = client.get_price_estimates(
			start_latitude = startLat,
			start_longitude = startLong,
			end_latitude = endLat,
			end_longitude = endLong,
			seat_count = 2
		)
		estimatedPrice = response.json.get('prices')
		randomString = "".join(random.choice(string.ascii_uppercase) for _ in range(10))
		for i in estimatedPrice:
			if(i['localized_display_name'] == "UberGo"):
				totalCost = (float(i['low_estimate']) + float(i['high_estimate'])) / 2
				totalTime = float(i['duration'])
				toReturn = {
					"route": [{
						"name": startName,
						"cost": 0,
						"mode": "NA"
					},{
						"name": endName,
						"cost": totalCost,
						"mode": "CAB"
					}],
					"totalCost": totalCost,
					"totalTime": totalTime // 60,
					"randomString": randomString	
				}
				return toReturn

		return {
			"route": [{
				"name": startName,
				"cost": 0,
				"mode": "NA"
			},{
				"name": endName,
				"cost": 10000000000,
				"mode": "CAB"
			}],
			"totalCost": 10000000000,
			"totalTime": 10000000000,
			"randomString": randomString
		}