billigst = -1
for j in range(0,2):
	start = j
	if (start+5) > 10:
			break
	summen = 0
	for x in range(start,start+5):
		print(x, " " , end="")
		summen += x
	print("summen:", summen)
	if billigst > summen or billigst == -1:
		billigst = summen
	#print(j, " " , end="")
print("billigst:", billigst)

