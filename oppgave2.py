import sys
import matplotlib.pyplot as plt
import random


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

	print("****** Assignment 1 - Task 2 - RTP ******")
	print("Which appliances would you like to start? ;")
	x = 1
	while True:
		print("[%d] %s" % (x, applianceLib[str(x)]["name"]))
		x += 1
		if x > len(applianceLib): break
	print("ex.: '1 2 3'")

	inputs = input("Appliances: ").split(" ")
	if len(inputs) > len(applianceLib):
		print("Too many arguments.")
		sys.exit()

	appliances = {}

	
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
	








