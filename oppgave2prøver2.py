import sys
import matplotlib.pyplot as plt
import random
from scipy.optimize import linprog
import time


def askFortime(message, which, length, a):
	"""
	Gets alphas and betas from the user
	"""

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


def printSchedule(res,apps):
	"""
	Prints the schedule
	"""
	x=res.x

	print("---------------------------------------------------------------- ")
	print(" ")
	print(" ")
	print("The optimized schedule:")
	print(" ")
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

	print(" ")
	print("The optimized schedule gives a daily energy price of " + str(res.fun)+",-")

def calculate(appliances, timeslots):
	"""
	Uses scipy linprog solver to minimize the function.
	Function creates all matrixes and constraints first, 
	then fills them with information from user/applianceLib. 

	"""
	print("Creating matrixes and constraints")

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

	# Run the solver
	print("running the solver")
	res = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq,b_eq=b_eq)
	# Print the schedule
	return res, apps



def generatePrice(timeslots):
	"""
	Generates price array using RTP
	"""
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

	# Generating price array
	timeslots = []
	timeslots = generatePrice(timeslots)

	# Appliances
	applianceLib = {			
				"1": {"name": "Electrical vehicle", "kwh" : 9.9, "length":6,"a":10, "b":18, "shiftable":True},
				"2": {"name": "Washing machine", "kwh" : 1.94, "length": 2, "a":12, "b":15, "shiftable":True},
				"3": {"name": "Dishwasher", "kwh" : 1.44, "length": 1, "a":21, "b":24, "shiftable":True},
				"4": {"name": "Cloth dryer", "kwh" : 2.50, "length": 6, "a":10, "b":24, "shiftable":True},
				"5": {"name": "Lighting", "kwh" : 1.50, "length": 10, "a":10, "b":20, "shiftable":False},
				"6": {"name": "Heating", "kwh" : 8.50, "length": 24, "a":0, "b":24, "shiftable":False},
				"7": {"name": "Refrigerator-freezer", "kwh" : 1.32, "length": 24, "a":0, "b":24, "shiftable":False},
				"8": {"name": "Electric stove", "kwh" : 3.90, "length": 2, "a":17, "b":19, "shiftable":False},
				"9": {"name": "TV", "kwh" : 0.32, "length": 5, "a":18, "b":23, "shiftable":False},
				"10": {"name": "Computer", "kwh" : 0.60, "length": 6, "a":8, "b":14, "shiftable":False},
				"11": {"name": "Cellphone charger", "kwh" : 0.05, "length": 3, "a":1, "b":4, "shiftable":False},
				"12": {"name": "Ceiling fan", "kwh" : 0.75, "length": 3, "a":0, "b":23, "shiftable":True},
				"13": {"name": "Router", "kwh" : 0.06, "length": 24, "a":0, "b":24, "shiftable":False},
				"14": {"name": "Coffee Maker", "kwh" : 0.80, "length":1,"a":0, "b":0, "shiftable":True},
				"15": {"name": "Hair Dryer", "kwh" : 1.50, "length":1,"a":0, "b":0, "shiftable":True},
				"16": {"name": "Toaster", "kwh" : 1.2 , "length":1,"a":0, "b":0, "shiftable":True},
				"17": {"name": "Iron", "kwh" : 1.1, "length": 1,"a":0, "b":0, "shiftable":True}
			}

	appliances = {}

	# Adding default appliances
	for x in range(1,14):
		appliances[x] = applianceLib[str(x)]
	
	
	print("****** Assignment 1 - Task 2 - RTP ******")
	print("These appliances have allready been added to your schedule: Electrical vehicle, Washing machine, Dishwasher, Cloth dryer, Lighting, Heating, Refrigerator-freezer, Electric stove, TV, Computer, Cellphone charger,Ceiling fan, Router")
	print("Add additional appliances:")
	x = 14
	while True:
		print("[%d] %s" % (x, applianceLib[str(x)]["name"]))
		x += 1
		if x > len(applianceLib): break
	print("ex.: '14 15 17'")
	
	
	
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
	
	n = 14		

	# Get alphas and betas from user
	for x in inputs:
		appliances[n] = applianceLib[x]

		# Get setup time
		if appliances[n]["shiftable"] == True:
			message =  "Setup time for " + appliances[n]["name"]
			start = askFortime(message, True, appliances[n]["length"],appliances[n]["a"])
			appliances[n]["a"] = start

			# Get deadline
			message =  "Deadline for " + appliances[n]["name"]
			deadline = askFortime(message, False, appliances[n]["length"],appliances[n]["a"])
			appliances[n]["b"] = deadline
			n += 1
		print()
	
	print()
	
	# Calculate the schedule
	print("Calculating schedule using linear programming. This can take some time... ")
	start = time.time()
	x,a = calculate(appliances, timeslots)
	end = time.time()
	print("The calculation used " + str(end-start)+" seconds")
	print(" ")
	printSchedule(x, a)

	#calculate(appliances, timeslots)
	








