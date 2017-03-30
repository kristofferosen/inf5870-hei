import sys
import matplotlib.pyplot as plt
import random
from scipy.optimize import linprog


def askFortime(message, which, length, a):

	time = -1

	# Setup 
	if which:
		while True:
			time = int(input("%s time (0-23): " % (message)))
			if time < 0 or time > 23:
				print("Timeslots needs to be between 0 and 3\n")
			else:
				break
	#Deadline
	else:
		while True:
			time = int(input("%s time (1-24): " % (message)))
			if time < 1 or time > 24:
				print("Timeslots needs to be between 2 and 24\n")
			elif time - a < length:
				print("Appliances needs more time than this to finish the job\n")
			else:
				break

	return time

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

def printSchedule(x,apps):
	"""
	Prints the schedule
	"""
	print(x)
	schedule = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23]]
	for k in range(int(len(x)/24)):
		for y in range(24):
			if x[y+(k*24)] != 0:
				schedule[y].append(apps[k])

	for hour in schedule:
		line = str(hour.pop(0)) + ":00 - "
		for appliance in hour:
			line += "| "
			line += appliance 
			line += " |"
		print(line)


def calculate(appliances, timeslots):
	"""
	Uses scipy linprog solver to minimize the function.
	Function creates all matrixes and constraints first, 
	then fills them with information from user/applianceLib. 

	"""
	print(appliances)
	aux =[]									# Helping variables
	apps=[]


	for i in range(len(appliances)):		# Create coefficients for objective function using the price array
		aux = aux + timeslots

	c = aux									# Objective function coefficients	
	A_eq = [[0]]*len(appliances)			# Equality matrix
	b_eq=[]									# Equality constraints 
	A = [[0]]*(24*len(appliances))			# Inequality matrix
	b = [0]*(24*len(appliances))			# Inequality constraints


	for i in range(len(appliances)):		# Filling equality matrix with 0s
		A_eq[i] = [0]*len(c)

	for i in range(24*len(appliances)):		# Filling inequality matrix with 0s
		A[i] = [0]*len(c)


	#For each appliance, fill in correct information in matrixes and constraints
	for key, appliance in appliances.items(): 
		apps.append(appliance["name"])
		b_eq.append(appliance["kwh"])
		x=0
		for j in range(appliance["a"]+(int(key)-1)*24,appliance["b"]+(int(key)-1)*24):
			A_eq[int(key)-1][j] = 1															
			A[x+(int(key)-1)*24+appliance["a"]][j] = 1
			b[j]=appliance["kwh"]/appliance["length"]
			x=x+1

	print(b)
	print(b_eq)
	print(c)

	# Run the solver
	res = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq,b_eq=b_eq, options={"disp": True})

	# Print the schedule
	printSchedule(res.x, apps)



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
	plt.title("Task 2 - Pricing curve")
	plt.grid(True)
	
	plt.plot(times, timeslots)
	plt.savefig("Task 2 - Pricing curve.png")

	#plt.show()
	plt.close()
	return timeslots
	

if __name__ == '__main__':
	timeslots = []
	timeslots = generatePrice(timeslots)

	applianceLib = {			
					"1": {"name": "Electrical vehicle", "kwh" : 9.9, "length":6,"a":0, "b":0, "shiftable":True},
					"2": {"name": "Washing machine", "kwh" : 1.94, "length": 2, "a":0, "b":0, "shiftable":True},
					"3": {"name": "Dishwasher", "kwh" : 1.44, "length": 1, "a":0, "b":0, "shiftable":True}					
					}

	appliances = {}

	for x in range(1,3):
		appliances[x] = applianceLib[str(x)]

	print("****** Assignment 1 - Task 2 - RTP ******")
	print("These appliances have allready been added to your schedule: Electrical vehicle, Washing machine, Dishwasher, Cloth dryer, Lighting, Heating, Refrigerator-freezer, Electric stove, TV, Computer, Cellphone charger,Ceiling fan, Router")
	print("Add additional appliances:")
	x = 3
	while True:
		print("[%d] %s" % (x, applianceLib[str(x)]["name"]))
		x += 1
		if x > len(applianceLib): break
	print("ex.: '1 2 3'")

	while(True):
		inputs = input("Appliances: ").split(" ")

		ok = True
		for x in inputs:
			if int(x) > 17:
				print("Invalid arguments")
				ok = False

		if len(inputs) > len(applianceLib):
			print("Too many arguments.")
		elif ok:
			break
			
	for x in inputs:
		appliances[x] = applianceLib[x]

		# Get setup time
		if appliances[x]["shiftable"] == True:
			message =  "Setup time for " + appliances[x]["name"]
			start = askFortime(message, True, appliances[x]["length"],appliances[x]["a"])
			appliances[x]["a"] = start

			# Get deadline
			message =  "Deadline for " + appliances[x]["name"]
			deadline = askFortime(message, False, appliances[x]["length"],appliances[x]["a"])
			appliances[x]["b"] = deadline

		print()
	
	print()

	calculate(appliances, timeslots)
	








