from util import util
from GraphAlgorithms import GraphAlgorithms
import time

class GraphMaker:
	stops = dict()
	adjList = [[dict() for j in range(2)] for i in range(1000 + 1)]
	otherMapping = dict()
	stopsDict = dict()
	nameToIndex = dict()
	indexToName = dict()
	mappingOfMetro = dict()
	reverseMappingOfMetro = dict()
	coor = dict()
	type = dict()
	countOfStops = 1
	graphAlgorithms = GraphAlgorithms()
	dist = [[0 for i in range(250)] for j in range(250)]

	def work(self, maxN):
		self.maxN = maxN
		busTrips = []

		util.trace("** Getting distance between every pair of metro stations **")
		self.dist = self.graphAlgorithms.floydWarshall(self.dist)

		# for i in range(1):
		# 	for j in range(220):
		# 		if(self.dist[i][j] != 0):
		# 			print self.dist[i][j]
		# 	print ()

		util.trace("** Adding bus trips to array. **")
		busTrips = self._addBusTrips()

		util.trace("** Adding bus stops to dict. **")
		self._addToDict(busTrips)

		util.trace("** Mapping the metro stations to numbers **")
		self._metroStationToNumbers()


		util.trace("** Adding metro trips **")
		metroTrips = self._addMetroTrips()

		util.trace("** Indexing the stops **")
		self._indexing()

		util.trace("** Making the edges between bus trips **")
		self._addBusEdges(busTrips)

		util.trace("** Making the graph of metro **")
		self._readEdges()

		util.trace("** Making the edges between metro trips ** ")
		self._addMetroEdges(metroTrips)

		util.trace("** Adding the coordinates **")
		self._addCoordinates()

		util.trace("** Dividing the values of edges be their counts **")
		self._manageValues()

		util.trace("** Making the stops dictionary containing all the properties of the stops. **")
		for i in self.stopsDict:
			if(i in self.coor and i in self.type):
				self.stops[i] = {
					"name": i,
					"coordinates": self.coor[i],
					"type": self.type[i],
					"nearestStop": "yet_to_be_defined",
					"index": self.nameToIndex[i]
				}

		util.trace("** Finding the nearest station from all the stops. **")
		self._setNearestStops()
		util.trace("** Adding the edges between the nearest stops. **")
		self._addRemainingEdges()
		return 1

	# Private functions
	def _addBusTrips(self):
		spamreader = open('assets/BusRouteTripData.csv', "rt")
		busTrips = []
		for row in spamreader:
			splitted_row = util.makeRow(row)
			busTrips.append(splitted_row)
			if(len(busTrips) > self.maxN):
				break

		return busTrips[1:]

	def _addToDict(self, busTrips):
		for i in busTrips:
			i[1] = i[1].lower()
			i[3] = i[3].lower()
			self.stopsDict[i[1]] = 1
			self.stopsDict[i[3]] = 1
			self.type[i[1]] = "BUS"
			self.type[i[3]] = "BUS"

	def _indexing(self):
		for i in self.stopsDict:
			self.nameToIndex[i] = self.countOfStops
			self.indexToName[self.countOfStops] = i
			self.countOfStops += 1

	def _metroStationToNumbers(self):
		spamreader = open('assets/StationNameToNumber.csv', "rt")
		cnt = 0
		for row in spamreader:
			if(cnt >= 3):
				splitted_row = util.makeRow(row)
				metroStationName = splitted_row[3].lower()
				self.otherMapping[metroStationName] = int(splitted_row[2])
				done = False
				for stop in self.stopsDict:
					if(util.equal(stop, "metro") and util.equal(stop, metroStationName)):
						done = True
						# util.trace(metroStationName)
						self.mappingOfMetro[int(splitted_row[2])] = stop
						self.reverseMappingOfMetro[stop] = int(splitted_row[2])
						self.type[stop] = "BOTH"
						break

				if(not done):
					for stop in self.stopsDict:
						if(util.equal(stop, metroStationName)):
							# util.trace(metroStationName)
							done = True
							self.mappingOfMetro[int(splitted_row[2])] = stop
							self.reverseMappingOfMetro[stop] = int(splitted_row[2])
							self.type[stop] = "BOTH"
							break

				if(not done):
					self.stopsDict[metroStationName] = 1
					self.mappingOfMetro[int(splitted_row[2])] = metroStationName
					self.reverseMappingOfMetro[metroStationName] = int(splitted_row[2])
					self.type[metroStationName] = "METRO"
			cnt += 1

	def _addMetroTrips(self):
		metroTrips = []
		spamreader = open('assets/MetroRouteTripData.csv', "rt")
		cnt = 0
		for row in spamreader:
			if(cnt >= 1):
				splitted_row = util.makeRow(row)
				metroTrips.append(splitted_row)
			cnt += 1
			if(cnt >= self.maxN):
				break

		return metroTrips

	def _addBusEdges(self, busTrips):
		for i in busTrips:
			fromStation = i[1]
			toStation = i[3]
			startTime = i[2]
			cost = int(i[-1])
			startTime = startTime[-8:]
			timeDiff = util.findTimeDiff(i[2], i[4])
			mode = i[0]
			if(cost % 5 != 0):
				cost = (cost // 5 + 1) * 5
			self._add(self.adjList[self.nameToIndex[fromStation]][0], self.nameToIndex[toStation], {
				"to": self.nameToIndex[toStation],
				"startTime": startTime,
				"time": timeDiff,
				"cost": int(cost),
				"count": 1,
				"mode": mode
			})
			self._add(self.adjList[self.nameToIndex[toStation]][0], self.nameToIndex[fromStation], {
				"to": self.nameToIndex[fromStation],
				"startTime": startTime,
				"time": timeDiff,
				"cost": int(cost),
				"count": 1,
				"mode": mode
			})

	def _addMetroEdges(self, metroTrips):
		for i in metroTrips:
			i[3] = i[3][:-1]
			fromStation = self.mappingOfMetro[int(i[0])].lower()
			toStation = self.mappingOfMetro[int(i[2])].lower()
			timeDiff = util.findTimeDiff(i[1], i[3])
			startTime = i[1][-12:-4]
			if(fromStation in self.reverseMappingOfMetro and toStation in self.reverseMappingOfMetro):
				fromStationMetroIdx = self.reverseMappingOfMetro[fromStation]
				toStationMetroIdx = self.reverseMappingOfMetro[toStation]
				distance = self.dist[fromStationMetroIdx][toStationMetroIdx]
				cost = self._getCost(distance)
			else:
				cost = 1e5

			self._add(self.adjList[self.nameToIndex[fromStation]][1], self.nameToIndex[toStation], {
				"to": self.nameToIndex[toStation],
				"startTime": startTime,
				"time": timeDiff,
				"cost": int(cost),
				"count": 1,
				"mode": "METRO"
			})
			self._add(self.adjList[self.nameToIndex[toStation]][1], self.nameToIndex[fromStation], {
				"to": self.nameToIndex[fromStation],
				"startTime": startTime,
				"time": timeDiff,
				"cost": int(cost),
				"count": 1,
				"mode": "METRO"
			})

	# Note: This _indexing only works if maxN = 1e6.
	def _addCoordinates(self):
		spamreader = open('assets/coordinates.txt', "rt")
		for row in spamreader:
			row = row[:-1]
			splitted_row = row.split(' ')
			idx = int(splitted_row[0])
			lng = float(splitted_row[-1])
			lat = float(splitted_row[-2])
			if(int(idx) >= self.countOfStops):
				break
			name = self.indexToName[int(idx)]
			self.coor[name] = {
				"lat": lat,
				"lng": lng
			}

	def _add(self, a, param, b):
		if(b["to"] in a):
			a[param]["cost"] += b["cost"]
			a[param]["time"] += b["time"]
			a[param]["count"] += b["count"]
		else:
			a[param] = b
		return a

	def _manageValues(self):
		for i in range(1000):
			for j in range(2):
				for tmp in self.adjList[i][j]:
					v = self.adjList[i][j][tmp]
					if(v["count"]):
						v["cost"] /= v["count"]
						v["time"] /= v["count"]

	def _setNearestStops(self):
		for tmp in self.stops:
			stop = self.stops[tmp]
			minDiff = 1000
			for tmp1 in self.stops:
				otherStop = self.stops[tmp1]
				if(stop["type"] != otherStop["type"] or stop["type"] == "BOTH"):
					startLat = stop["coordinates"]["lat"]
					startLong = stop["coordinates"]["lng"]
					endLat = otherStop["coordinates"]["lat"]
					endLong = otherStop["coordinates"]["lng"]
					if(minDiff > util.squaredDistance((startLat, startLong), (endLat, endLong))):
						minDiff = util.squaredDistance((startLat, startLong), (endLat, endLong))
						nearestStop = tmp1
			self.stops[tmp]["nearestStop"] = nearestStop

	def _addRemainingEdges(self):
		for tmp in self.stops:
			stopIdx = self.stops[tmp]["index"]
			otherStopName = self.stops[tmp]["nearestStop"]
			otherStopIdx = self.nameToIndex[otherStopName]

			if(self.stops[tmp]["type"] == "BUS" and otherStopIdx not in self.adjList[stopIdx][0]):
				for time in range(4):
					timeStr = str(time * 6)
					if(len(timeStr) == 1):
						timeStr = "0" + timeStr
					timeStr += ":00:00"
					# print(timeStr)
					self.adjList[stopIdx][0][otherStopIdx] = {
						"to": otherStopIdx,
						"startTime": timeStr,
						"time": 5,
						"cost": 0,
						"count": 1,
						"mode": "WALK"
					}



	def _readEdges(self):
		spamreader = open("assets/metroMap.txt", "rt")
		for row in spamreader:
			row = row.lower()
			inp = row.split(',')
			for i in range(len(inp)):
				if(i >= 1):
					if inp[i] in self.reverseMappingOfMetro and inp[i - 1] in self.reverseMappingOfMetro:
						# print(inp[i])
						startStopIdxInSheet = self.reverseMappingOfMetro[inp[i]]
						endStopIdxInSheet = self.reverseMappingOfMetro[inp[i - 1]]
						self.dist[startStopIdxInSheet][endStopIdxInSheet] = 1

						startStopName = self.mappingOfMetro[startStopIdxInSheet]
						endStopName = self.mappingOfMetro[endStopIdxInSheet]

						startIdx = self.nameToIndex[startStopName]
						endIdx = self.nameToIndex[endStopName]

						# print(startIdx, endIdx)

	def _getCost(self, distance):
		return min(60, (distance // 5 + 1) * 10)

	# def _addEdgesOfMetroStations(self):
	# 	for i in range(250):
	# 		for j in range(250):
	# 			u = self.mappingOfMetro[i]
	# 			v = self.mappingOfMetro[j]
	# 			startIndex = self.nameToIndex[self.mappingOfMetro[i]]
	# 			endIndex = self.nameToIndex[self.mappingOfMetro[j]]

	# 			distance = self.dist[u][v]
	# 			cost = self._getCost(distance)
	# 			self._add(self.adjList[startIndex][1], self.endIndex, {
	# 				"to": endIndex,
	# 				"startTime": 
	# 			})

	# 			for time in range(1, 4):
	# 				timeStr = str(time * 6)
	# 				if(len(timeStr) == 1):
	# 					timeStr = "0" + timeStr
	# 				timeStr += ":00:00"
	# 				# print(timeStr)
	# 				self._add(self.adjList[startIndex][1], endIndex, {
	# 					"to": self.nameToIndex[toStation],
	# 					"startTime": startTime,
	# 					"time": timeDiff,
	# 					"cost": int(cost),
	# 					"count": 1,
	# 					"mode": "METRO"
	# 				})
