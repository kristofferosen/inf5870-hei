import sys

def askFortime(message):
	time = int(input("%s time (0-23): " % (message)))
	if time < 0 or time > 23:
		print("Timeslots needs to be between 0 and 23\n")
		return -1
	return time

def calculate(appliances, timeslots):
	for element in appliances:
		if len(element) == 3:
			continue
		if 1.0 in timeslots[element[3]:element[4]]:
			print("The given time area are during high energy cost.")
		else:
			print("You have the minimied enery cost")

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

	appliances = []
	appliances.append(["1", "Washing machine", 1.94])
	appliances.append(["2", "Electrical vehicle (EV)", 9.9])
	appliances.append(["3", "Dishwasher", 1.44])


	timeslots = [0.5] * 24
	for i in range(17,21):
		timeslots[i] = 1.0

	status = False
	
	for x in inputs:
		print("\n%s - %s:" % (appliances[int(x)-1][0], appliances[int(x)-1][1]))
		start = askFortime("Start")
		if start == -1:
			status = True
			break
		appliances[int(x)-1].append(start)
		deadline = askFortime("Deadline")
		if deadline == -1:
			status = True
			break
		appliances[int(x)-1].append(deadline)
	
	if status == True:
		print("ERROR!!!")
		sys.exit()

	print()
	for x in appliances:
		print(x)
	print()


	calculate(appliances, timeslots)
	








