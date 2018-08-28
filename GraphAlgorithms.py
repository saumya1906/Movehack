import heapq, string, random
from util import util

class GraphAlgorithms:
	def floydWarshall(self, edge):
		dist = [[0 for i in range(250)] for j in range(250)]
		for i in range(250):
			for j in range(250):
				dist[i][j] = edge[i][j]

		for i in range(250):
			for j in range(250):
				for k in range(250):
					dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

		return dist


	def djsktra(self, start, end, g, comparator, otherComparator, indexToName, startTime):
		self.g = g
		self.start = start
		self.end = end
		self.comparator = comparator
		self.otherComparator = otherComparator
		self.indexToName = indexToName
		self.startTime = startTime
		return self._runDjsktra()

	def _runDjsktra(self):
		pq = []
		vis = [False for i in range(1000)]
		dist = [1e12 for i in range(1000)]
		otherDist = [1e12 for i in range(1000)]
		bus = ["" for i in range(1000)]
		par = [-1 for i in range(1000)]
		heapq.heapify(pq)
		heapq.heappush(pq, [0, self.start, "NA", 0])
		vis[self.start] = True
		dist[self.start] = 0
		otherDist[self.start] = 0
		while(len(pq) != 0):
			nextVertex = heapq.heappop(pq)
			u = nextVertex[1]
			weightTillNow = nextVertex[0]
			otherWeight = nextVertex[3]
			vis[u] = True
			prevRoute = nextVertex[2]
			offset = 200
			if(u == self.end):
				break
			# Bus trips:
			for tmp in self.g[u][0]:
				v = self.g[u][0][tmp]
				if(not vis[v["to"]]):
				# and util.sameHour(v["startTime"], self.startTime)):
					if(dist[v["to"]] > weightTillNow + v[self.comparator] + (offset if v["mode"] != prevRoute and prevRoute != "NA" and self.comparator == "time" else 0)):
						dist[v["to"]] = weightTillNow + v[self.comparator] + (offset if v["mode"] != prevRoute and prevRoute != "NA" and self.comparator == "time" else 0)
						# print(v["to"], self.otherComparator)
						otherDist[v["to"]] = otherWeight + v[self.otherComparator] + (offset if v["mode"] != prevRoute and prevRoute != "NA" and self.comparator != "time" else 0)
						heapq.heappush(pq, [dist[v["to"]], v["to"], v["mode"], otherDist[v["to"]]])
						par[v["to"]] = u
						bus[v["to"]] = v["mode"]

			for tmp in self.g[u][1]:
				v = self.g[u][1][tmp]
				if(not vis[v["to"]]):
					if(dist[v["to"]] > weightTillNow + v[self.comparator] + (offset if v["mode"] != prevRoute and prevRoute != "NA" and self.comparator == "time" else 0)):
						dist[v["to"]] = weightTillNow + v[self.comparator] + (offset if v["mode"] != prevRoute and prevRoute != "NA" and self.comparator == "time" else 0)
						otherDist[v["to"]] = otherWeight + v[self.otherComparator] + (offset if v["mode"] != prevRoute and prevRoute != "NA" and self.comparator != "time" else 0)
						heapq.heappush(pq, [dist[v["to"]], v["to"], "METRO", otherDist[v["to"]]])
						par[v["to"]] = u
						bus[v["to"]] = "METRO"

		toReturn = []
		tmp = self.end
		while(par[tmp] != -1):
			toReturn.append({
				"name": self.indexToName[tmp],
				"cost": (dist[tmp] if self.comparator == "cost" else otherDist[tmp]),
				"mode": bus[tmp]
			})
			tmp = par[tmp]

		toReturn.append({
			"name": self.indexToName[tmp],
			"cost": 0,
			"mode": "start"
		})
		toReturn.reverse()
		lastValCost = 0
		totalCost = dist[self.end]
		otherTotalCost = otherDist[self.end]
		self.randomString = "".join(random.choice(string.ascii_uppercase) for _ in range(10))

		actualToReturn = {
			"route": toReturn,
			"totalTime": (totalCost // 60 if self.comparator == "time" else otherTotalCost // 60),
			"totalCost": (totalCost if self.comparator == "cost" else otherTotalCost),
			"randomString": self.randomString
		}

		for val in toReturn:
			lastValCostTmp = val["cost"]
			val["cost"] -= lastValCost
			lastValCost = lastValCostTmp

		return actualToReturn