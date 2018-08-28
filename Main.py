import csv, json, time, datetime, sys
from util import util
from PreProcesser import PreProcesser
from ApiHandler import ApiHandler
from GraphAlgorithms import GraphAlgorithms
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

class Main:

	def __init__(self):
		self.preProcesser = PreProcesser()
		self.preProcesser.preProcess(maxN = 100000)
		self.nameToIndex = self.preProcesser.graphMaker.nameToIndex
		self.indexToName = self.preProcesser.graphMaker.indexToName
		self.g = self.preProcesser.graphMaker.adjList
		self.graphAlgorithms = GraphAlgorithms()
		# print(self.g[1])

	def makeCoordinateValues(self, stops):
		# print(stops)
		ct = 0
		for i in stops:
			stop = stops[i]
			ct += 1
			if(ct < 800):
				continue
			copyStop = stop["name"]
			copyStop += " delhi"
			response = util.hitApi("https://maps.googleapis.com/maps/api/geocode/json?address=" + copyStop + "&key=AIzaSyBpMr3IX_arUxqVsksiKBCUwDMnOO1moRI")
			if(response['status'] == "OK"):
				lat = response['results'][0]['geometry']['location']['lat']
				lng = response['results'][0]['geometry']['location']['lng']
				print ct, stop["name"], lat, lng
				util.trace(ct)

	def _getNearestStation(self, coor, inputType, stops):
		minDiff = 100
		for i in stops:
			if(stops[i]["type"] == inputType or inputType == "BOTH"):
				stopLat = stops[i]["coordinates"]["lat"]
				stopLong = stops[i]["coordinates"]["lng"]
				if(minDiff > util.squaredDistance((stopLat, stopLong), coor)):
					minDiff = util.squaredDistance((stopLat, stopLong), coor)
					ans = stops[i]
		return ans

	def solve(self, startStation, endStation):
		startCoordinates = ApiHandler.getCoordinates(startStation)
		endCoordinates = ApiHandler.getCoordinates(endStation)

		startMetro = self._getNearestStation((startCoordinates["lat"], startCoordinates["lng"]), "METRO", self.preProcesser.graphMaker.stops)
		endMetro = self._getNearestStation((endCoordinates["lat"], endCoordinates["lng"]), "METRO", self.preProcesser.graphMaker.stops)
		startTime = datetime.datetime.now()
		startTime = str(startTime)[-15:-7]

		# print(startMetro, endMetro)
		
		timeRoute = self.graphAlgorithms.djsktra(self.nameToIndex[startMetro["name"]], self.nameToIndex[endMetro["name"]], self.g, "time", "cost", self.indexToName, startTime)
		costRoute = self.graphAlgorithms.djsktra(self.nameToIndex[startMetro["name"]], self.nameToIndex[endMetro["name"]], self.g, "cost", "time", self.indexToName, startTime)
		comfortRoute = ApiHandler.uberGoPrice(startCoordinates["lat"], startCoordinates["lng"], endCoordinates["lat"], endCoordinates["lng"], startStation, endStation)

		toReturn = {
			"timeRoute": timeRoute,
			"costRoute": costRoute,
			"comfort": comfortRoute
		}

		print timeRoute
		print '\n'
		print costRoute
		print '\n'
		print comfortRoute

		return toReturn
		# startIndex = self.preProcesser.graphMaker.nameToIndex[startMetro["name"]]
		# endIndex = self.preProcesser.graphMaker.nameToIndex[endMetro["name"]]
		# uberGo = ApiHandler.uberGoPrice(startCoordinates["lat"], startCoordinates["lng"], endCoordinates["lat"], endCoordinates["lng"])

# main = Main()
# main.solve("IIT delhi", "IIIT delhi, okhla")

# To-do
# Get the metro api for getting cost between two stations and add them to graphs.
# Get the uber api for getting cost between two locations - best comfort zone.
# Traverse over all coordinates to get the nearest metro station or bus stop.
# Run djisktra on the graph made by the bus and metro tickets people have.
# Includes: by cost, by comfort, by time, by mixtures of these, least number of changes, metro line changing should also be included.