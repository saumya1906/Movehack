import requests, sys

class util:
	@staticmethod
	def makeRow(row):
		ct = 0
		s = ""
		L = []
		for i in range(len(row)):
			if((row[i] == ',' or i == len(row) - 1) and ct == 0):
				if(i >= len(row) - 1):
					s += row[i]
					t = ""
					for j in s:
						if(j != "\"" and j != '\n'):
							t += j
					L.append(t)
					break
				t = ""
				for j in s:
					if(j != "\""):
						t += j
				L.append(t)
				s = ""
			s += row[i]
			if(s[0] == ','):
				s = ""
			if(row[i] == "\""):
				ct = 1 - ct
		return L

	@staticmethod
	def swap(s1, s2):
		tmp = s1
		s1 = s2
		s2 = tmp

	@staticmethod
	def equal(s1, s2):
		if(len(s1) < len(s2)):
			util.swap(s1, s2)
		for i in range(len(s1) - len(s2) + 1):
			if(s1[i: i + len(s2)] == s2 and (i + len(s2) == len(s1) or s1[i + len(s2)] == " ")):
				return True
		return False

	@staticmethod
	def findTimeDiff(t1, t2):
		if(t1[-4] == '.'):
			t1 = t1[-12:-4]
			t2 = t2[-12:-4]
		else:
			t2 = t2[-8:]
			t1 = t1[-8:]
		# print(t1, t2)
		hourStart, minuteStart, secondStart = int(t1[0] + t1[1]), int(t1[3] + t1[4]), int(t1[6] + t1[7])
		hourEnd, minuteEnd, secondEnd = int(t2[0] + t2[1]), int(t2[3] + t2[4]), int(t2[6] + t2[7])
		startTime = hourStart * 3600 + minuteStart * 60 + secondStart
		endTime = hourEnd * 3600 + minuteEnd * 60 + secondEnd
		timeDiff = endTime - startTime
		if(timeDiff < 0):
			timeDiff += 24 * 60 * 60 * 60
		return timeDiff

	@staticmethod
	def hitApi(str):
		return (requests.get(str)).json()

	@staticmethod
	def trace(str):
		print >> sys.stderr, str

	@staticmethod
	def sameHour(time1, time2):
		return int(time1[:2]) // 4 == int(time2[:2]) // 4

	@staticmethod
	def squaredDistance(a, b):
		return (a[0] - b[0]) * (a[0] - b[0]) + (a[1] - b[1]) * (a[1] - b[1])
