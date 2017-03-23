import sys
import matplotlib.pyplot as plt
import random
import os


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


def calculate(appliances, timeslots, houseNumber):

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

	with open("Task 3 - Households/" + str(houseNumber) + ".txt", 'a') as out:
		out.write("Household number: " + str(houseNumber))
		# Print the schedule
		for hour in schedule:
			line = str(hour.pop(0)) + ":00 - "
			for appliance in hour:
				line += "| "
				line += appliance 
				line += " |"
			print(line)
			out.write(line + "\n")
		out.write("\n")


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
	for elementList in listOfHouses:
		appliances = {}

		for x in elementList.keys():
			x = str(x)
			appliances[x] = applianceLib[x]

			# Get setup time
			if appliances[x]["shiftable"] == True:
				start, deadline = askFortime(appliances[x]["length"])
				appliances[x]["a"] = start
				appliances[x]["b"] = deadline
			print(appliances[x]["name"])
			print("*****************************************")

			print()
		
		print()

		calculate(appliances, timeslots, houseNumber)
		houseNumber += 1

