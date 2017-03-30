import sys
import matplotlib.pyplot as plt
import random
import os
from scipy.optimize import linprog
import time

def askFortime(length):
	"""
	Gives random alphas and betas
	"""

	time1 = 250
	time2 = 250
	while (time1 + length) > 23:
		time1 = random.randint(0, 23)
		time2 = random.randint(time1, 23)
	while (time2 - time1) < length:
		time2 = random.randint(time1, 23)

	return time1, time2


def printSchedule(bigx,apps):
	"""
	Prints the schedule
	"""

	houseNumber= 1
	n=0
	while(n < len(bigx)):
		x = bigx[n:n+(10*24)]
		schedule = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23]]
		for k in range(int(len(x)/24)):
			for y in range(24):
				if x[y+(k*24)] != 0:
					schedule[y].append(apps[k+(10*(houseNumber-1))])
		with open("Task 3 - Households/" + str(houseNumber) + ".txt", 'a') as out:
			out.write("Household number: " + str(houseNumber))
			out.write("\n")
			for hour in schedule:
				line = str(hour.pop(0)) + ":00 - "
				for appliance in hour:
					line += "| "
					line += appliance 
					line += " |"

				out.write(line + "\n")
		#out.write("\n")
		n += (10*24)
		houseNumber += 1

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
	print("Running the solver...")
	res = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq,b_eq=b_eq, options={"disp": True, "maxiter": 100000})

	# Print the schedule
	return res.x, apps




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
	plt.title("Task 3 - Pricing curve")
	plt.grid(True)
	
	plt.plot(times, timeslots)
	plt.savefig("Task 3 - Pricing curve.png")

	#plt.show()
	plt.close()

	return timeslots
	

if __name__ == '__main__':

	print("****** Assignment 1 - Task 3 - 30 households ******")

	# Generate the price array
	timeslots = []
	timeslots = generatePrice(timeslots)

	# Appliances
	applianceLib = {
					"1": {"name": "Electrical vehicle", "kwh" : 9.9, "length":6,"a":0, "b":0, "shiftable":True},
					"2": {"name": "Washing machine", "kwh" : 1.94, "length": 2, "a":0, "b":0, "shiftable":True},
					"3": {"name": "Dishwasher", "kwh" : 1.44, "length": 1, "a":0, "b":0, "shiftable":True},
					"4": {"name": "Cloth dryer", "kwh" : 2.50, "length": 6, "a":0, "b":0, "shiftable":True},
					"5": {"name": "Lighting", "kwh" : 1.50, "length": 10, "a":10, "b":20, "shiftable":False},
					"6": {"name": "Heating", "kwh" : 8.50, "length": 24, "a":0, "b":24, "shiftable":False},
					"7": {"name": "Refrigerator-freezer", "kwh" : 1.32, "length": 24, "a":0, "b":24, "shiftable":False},
					"8": {"name": "Electric stove", "kwh" : 3.90, "length": 2, "a":17, "b":19, "shiftable":False},
					"9": {"name": "TV", "kwh" : 0.32, "length": 5, "a":18, "b":23, "shiftable":False},
					"10": {"name": "Computer", "kwh" : 0.60, "length": 6, "a":8, "b":14, "shiftable":False},
					"11": {"name": "Cellphone charger", "kwh" : 0.05, "length": 3, "a":1, "b":4, "shiftable":False},
					"12": {"name": "Ceiling fan", "kwh" : 0.75, "length": 3, "a":0, "b":0, "shiftable":True},
					"13": {"name": "Router", "kwh" : 0.06, "length": 24, "a":0, "b":24, "shiftable":False}
					}

	# Create folder for schedule files
	if os.path.exists("Task 3 - Households"):
		import shutil
		shutil.rmtree("Task 3 - Households", ignore_errors=False, onerror=None)

	os.makedirs("Task 3 - Households")


	houseNumber = 1
	appliances = {}
	n = 1
	listOfHouses = []

	# Choose appliances for 30 households
	for x in range(0,30):
		listOfHouseAppliances = {}
		for y in range(0,10):
			applianceID = random.randint(1, len(applianceLib))
			while str(applianceID) in listOfHouseAppliances.keys():
				applianceID = random.randint(1, len(applianceLib))
			listOfHouseAppliances.update({str(applianceID): applianceLib[str(applianceID)]})
		listOfHouses.append(listOfHouseAppliances)

	
	# Add information about appliances
	for elementList in listOfHouses:	
		for x in elementList.keys():
			x = str(x)
			appliances[n] = applianceLib[x]

			# Get setup time
			if appliances[n]["shiftable"] == True:
				start, deadline = askFortime(appliances[n]["length"])
				appliances[n]["a"] = start
				appliances[n]["b"] = deadline

			n+=1

		houseNumber += 1

	# Calculate the schedule
	print("Calculating schedule using linear programming. This can take some time... ")
	start = time.time()
	x,a = calculate(appliances, timeslots)
	end = time.time()
	print("The calculation used " + str(end-start)+" seconds")


	print("Printing schedule to the folder: ''Task 3 - Households''")
	printSchedule(x, a)

