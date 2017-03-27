import sys
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


def calculate(appliances, timeslots):
	aux = []

	for i in range(len(appliances)):
		aux = aux + timeslots
	
	c = aux
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
			A_eq[int(key)-1][j] = 1
			A[x+(int(key)-1)*24+appliance["a"]][j] = 1
			b[j]=appliance["kwh"]/appliance["length"]
			x=x+1

	res = linprog(c, A_ub=A, b_ub=b, A_eq=A_eq,b_eq=b_eq, options={"disp": True})
	print(res)

	print(len(res.x))



"""
	schedule = [[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23]]

	#Go through all appliances
	for key, appliance in appliances.items():
		a = appliance["a"]
		b = appliance["b"]
	
		# Calculate the best time to start the appliance
		start = optimize(timeslots[a:b], appliance)
	
		# Add to schedule
		for i in range(appliance["length"]):
			schedule[int(i+start)].append(appliance["name"])

	# Print the schedule
	for hour in schedule:
		line = str(hour.pop(0)) + ":00 - "
		for appliance in hour:
			line += "| "
			line += appliance 
			line += " |"
		print(line)
	"""

if __name__ == '__main__':
	print("****** Assignment 1 - Task 1 - ToU ******")
	print("Which appliances would you like to start? ;")
	print("\t[1] Washing machine")
	print("\t[2] Electrical vehicle (EV)")
	print("\t[3] Dishwasher")
	print("ex.: '1 2 3'")

	inputs = input("Appliances: ").split(" ")
	if len(inputs) > 3:
		print("Too many arguments.")
		sys.exit()

	applianceLib = {"1": {"name": "Electrical vehicle", "kwh" : 9.9, "length":6,"a":0, "b":0},
					"2": {"name": "Washing machine", "kwh" :  1.94, "length": 2, "a":0, "b":0},
					"3": {"name": "Dishwasher", "kwh" : 1.44, "length": 1, "a":0, "b":0}}		

	appliances = {}

	timeslots = [0.5] * 24
	for i in range(17,20):
		timeslots[i] = 1.0

	
	
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

	calculate(appliances, timeslots)
	








