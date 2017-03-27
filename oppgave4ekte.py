import sys
import matplotlib.pyplot as plt
import random
import os
from scipy.optimize import linprog


def askFortime(length):
	time1 = 250
	time2 = 250
	while (time1 + length) > 23:
		time1 = random.randint(0, 23)
		time2 = random.randint(time1, 23)
	while (time2 - time1) < length:
		time2 = random.randint(time1, 23)

	return time1, time2

def optimize(timeslots, appliance):

	
	fact = int(len(timeslots)-appliance["length"])+1	

	results = []
	for i in range(fact):
		xah = []
		for y in range(len(timeslots)):
			xah.append(0)
		for k in range(appliance["length"]):
			xah[k+i] = 1
		results.append(xah)

	lowest = [0,100000]
	x = 0
	for option in results:
		summ = 0 
		for i in range(len(option)):
			summ += option[i] * timeslots[i]

		if summ < lowest[1] and summ != lowest[1]:
			lowest[0] = x
			lowest[1] = summ

		x += 1

	return appliance["a"] + lowest[0]


def calculateFirst(appliances, timeslots):

	aux = []

	for i in range(len(appliances)):
		aux = aux + timeslots
	
	c = aux
	print(len(c))
	print(len(appliances))
	print("asjdhkasjd")
	A_eq = [[0]]*len(appliances)
	b_eq=[]
	A = [[0]]*(24*len(appliances))
	b = [0]*(24*len(appliances))
	for i in range(len(appliances)):
		A_eq[i] = [0]*len(c)

	for i in range(24*len(appliances)):
		A[i] = [0]*len(c)

	for key, appliance in appliances.items():
		b_eq.append(appliance["kwh"])
		x=0
		for j in range(appliance["a"]+(int(key)-1)*24,appliance["b"]+(int(key)-1)*24):
			print(j)
			print(appliance["name"])
			print(A_eq)
			print(len(A_eq[0]))
			A_eq[int(key)-1][j] = 1
			A[x+(int(key)-1)*24+appliance["a"]][j] = 1
			b[j]=appliance["kwh"]/appliance["length"]
			x=x+1

	res = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq,b_eq=b_eq, options={"disp": True})
	return res.x


def generatePrice(timeslots):
	times = []
	for i in range(0,24):
		times.append(i)
		timeslots.append(random.uniform(0.5, 1.0))	#Oppgave 2

	for j in range(6,10):							#Oppgave 2
		timeslots[j] = timeslots[j]*1.5				#Oppgave 2
	for k in range(17,21):
		timeslots[k] = timeslots[k]*2

	plt.figure()
	plt.xlabel("Timeslot")
	plt.ylabel("Price")
	plt.title("Task 3 - Pricing curve")
	plt.grid(True)
	
	plt.plot(times, timeslots)
	plt.savefig("Task 3 - Pricing curve.png")

	#plt.show()
	plt.close()

	return timeslots

def par(schedule):
	L_h = [0]*24
	houses = len(schedule)
	for i in range(houses):
		for y in range(len(schedule[i])):
			for k in range(len(schedule[i][y])):
				L_h[k] += schedule[i][y][k]
	peakHour = max(L_h)
	average = sum(L_h)/len(L_h)
	return peakHour/average

def setup(appliances):

	schedule = [[0]]*len(appliances)

	for key, appliance in appliances.items():
		schedule[int(key)] = [0]*24
		for x in range(appliance["a"], appliance["a"]+appliance["length"]):
			schedule[int(key)][x] = appliance["kwh"]
	return schedule
def findFirst(y):
	k = 0
	for x in y:
		if x != 0:
			return k
		k += 1
def doChange(a,first):
	if first + a[0] >= a[2]:
		return False
	else:
		return True


def minPar(s,h):
	change = False

	for x in range(len(s)):
		for y in range(len(s[x])):
			#y = schedule for et apperat i et hus
			first = findFirst(s[x][y])
			if doChange(h[x][y],first):
				#flytt en fram
				prevPar = par(s)

				tempY = list(y)
				tempS = list(s)

				new = move(y)

				tempS[x][y] = new

				newpar = par(tempS)


			


if __name__ == '__main__':
	timeslots = []
	timeslots = generatePrice(timeslots)

	applianceLib = {
					"1": {"name": "Electrical vehicle", "kwh" : 9.9, "length":6,"a":0, "b":0, "shiftable":True},
					"2": {"name": "Washing machine", "kwh" : 1.94, "length": 2, "a":0, "b":0, "shiftable":True},
					"3": {"name": "Dishwasher", "kwh" : 1.44, "length": 1, "a":0, "b":0, "shiftable":True},
					"4": {"name": "Cloth dryer", "kwh" : 2.50, "length": 6, "a":0, "b":0, "shiftable":True},
					"5": {"name": "Lighting", "kwh" : 1.50, "length": 10, "a":10, "b":20, "shiftable":False},
					"6": {"name": "Heating", "kwh" : 8.50, "length": 24, "a":0, "b":23, "shiftable":False},
					"7": {"name": "Refrigerator-freezer", "kwh" : 1.32, "length": 24, "a":0, "b":23, "shiftable":False},
					"8": {"name": "Electric stove", "kwh" : 3.90, "length": 2, "a":17, "b":19, "shiftable":False},
					"9": {"name": "TV", "kwh" : 0.32, "length": 5, "a":18, "b":23, "shiftable":False},
					"10": {"name": "Computer", "kwh" : 0.60, "length": 6, "a":8, "b":14, "shiftable":False},
					"11": {"name": "Cellphone charger", "kwh" : 0.05, "length": 3, "a":1, "b":4, "shiftable":False},
					"12": {"name": "Ceiling fan", "kwh" : 0.75, "length": 3, "a":0, "b":0, "shiftable":True},
					"13": {"name": "Router", "kwh" : 0.06, "length": 24, "a":0, "b":23, "shiftable":False}
					}

	print("****** Assignment 1 - Task 3 - 30 households ******")
	if os.path.exists("Task 3 - Households"):
		print("dsfs")
		import shutil
		shutil.rmtree("Task 3 - Households", ignore_errors=False, onerror=None)

	os.makedirs("Task 3 - Households")

	listOfHouses = []
	for x in range(0,30):
		listOfHouseAppliances = {}
		for y in range(0,5):
			applianceID = random.randint(1, len(applianceLib))
			while str(applianceID) in listOfHouseAppliances.keys():
				applianceID = random.randint(1, len(applianceLib))
			listOfHouseAppliances.update({str(applianceID): applianceLib[str(applianceID)]})
		listOfHouses.append(listOfHouseAppliances)

	houseNumber = 1
	schedule = []
	houses = []
	for elementList in listOfHouses:
		appliances = {}
		k = 0
		print(elementList)
	
		empty=[[0,0]]*len(elementList)
		houses.append(empty)
		for x in elementList.keys():
			x = str(x)
			appliances[str(k)] = applianceLib[x]

			# Get setup time
			if appliances[str(k)]["shiftable"] == True:
				start, deadline = askFortime(appliances[str(k)]["length"])
				appliances[str(k)]["a"] = start
				appliances[str(k)]["b"] = deadline
			print(appliances[str(k)]["length"])
			length = int(appliances[str(k)]["length"])

			houses[houseNumber-1][k][0]=int(appliances[str(k)]["length"])
			houses[houseNumber-1][k][1]=int(appliances[str(k)]["kwh"])
			houses[houseNumber-1][k][2]=int(appliances[str(k)]["b"])
			k += 1


		schedule.append(setup(appliances))
		houseNumber += 1

	parr=par(schedule)
	print(parr)
	print(houses)
	minimized = False
	while(minimized):
		minmized = minPar(schedule, houses)
