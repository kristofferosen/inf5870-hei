import sys


def compute(dws,dwd,wms,wmd,ts,td):
	print("Dishwasher kjores mellom kl " + str(dws) + " og kl " + str(dwd))
	print("Washing machine kjores mellom kl " + str(wms) + " og kl " + str(wmd))
	print("Tesla lades mellom kl " + str(ts) + " og kl " + str(td))







# Dishwasher 
dws = int(sys.argv[1])
dwd = int(sys.argv[2])

# Washing machine
wms = int(sys.argv[3])
wmd = int(sys.argv[4])

# Tesla
ts = int(sys.argv[5])
td = int(sys.argv[6])


compute(dws,dwd,wms,wmd,ts,td)

