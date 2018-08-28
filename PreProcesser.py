from GraphMaker import GraphMaker
import time
from util import util

class PreProcesser:
	def preProcess(self, maxN):
		start = time.clock()
		self.maxN = maxN
		self.graphMaker = GraphMaker()
		self.graphMaker.work(maxN = maxN)

		# for stop in self.graphMaker.stops:
		# 	print stop["name"]

		# # To-do
		# # Get the metro api for getting cost between two stations and add them to graphs.
		# # Get the uber api for getting cost between two locations - best comfort zone.
		# # Traverse over all coordinates to get the nearest metro station or bus stop.
		# # Run djisktra on the graph made by the bus and metro tickets people have.
		# # Includes: by cost, by comfort, by time, by mixtures of these, least number of changes, metro line changing should also be included.