import sys
from scipy.optimize import linprog
import time

def askFortime(message, which, length, a):
	"""
	Gets setup time and deadline for an specific appliance from the user.
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
	res = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq,b_eq=b_eq, options={"disp": True})
	
	# Print the schedule
	printSchedule(res, apps)


if __name__ == '__main__':

	# Set up interface
	print("****** Assignment 1 - Task 1 - ToU ******")
	print("These appliances are available:")
	print("\t[1] Washing machine")
	print("\t[2] Electrical vehicle (EV)")
	print("\t[3] Dishwasher")
	print(" ")
	print("Please input startup time and deadline for the appliances:")
	print(" ")
	print(" ")

	# Recive input
	inputs = ["1","2","3"]
	if len(inputs) > 3:
		print("Too many arguments.")
		sys.exit()

	appliances = {}

	# Information about the appliances
	applianceLib = {"1": {"name": "Electrical vehicle", "kwh" : 9.9, "length":6,"a":0, "b":0},
					"2": {"name": "Washing machine", "kwh" :  1.94, "length": 2, "a":0, "b":0},
					"3": {"name": "Dishwasher", "kwh" : 1.44, "length": 1, "a":0, "b":0}}		
	
	# Create price array (ToU)
	timeslots = [0.5] * 24
	for i in range(17,20):
		timeslots[i] = 1.0

	
	
	# Get setup time and deadline for all appliances
	for x in inputs:
		appliances[x] = applianceLib[x]

		# Get setup time
		message =  "Setup time for " + appliances[x]["name"]
		start = askFortime(message, True, appliances[x]["length"],appliances[x]["a"])
		appliances[x]["a"] = start

		# Get deadline
		message =  "Deadline for " + appliances[x]["name"]
		deadline = askFortime(message, False, appliances[x]["length"],appliances[x]["a"])
		appliances[x]["b"] = deadline
		print()
	
	print()

	# Calculate best schedule using linprog
	calculate(appliances, timeslots)
	








