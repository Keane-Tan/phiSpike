ori = open("AllSelections.txt","r")
j2 = open("AllSelections2.txt","w+")
j3 = open("AllSelections3.txt","w+")

j2.truncate(0)
j3.truncate(0)

cont2 = []
cont3 = []

cont = ori.readlines()

for i in range(len(cont)):
	if "[1]" in cont[i]:
		cont_2 = cont[i].replace("0.0345792","rad")
		cont_3 = cont[i].replace("[1]","[3]")
	else:
		cont_2 = cont[i]
		cont_3 = cont[i]

	cont2.append(cont_2)
	cont3.append(cont_3)

	j2.seek(0)
	j2.writelines(cont2)
	j2.truncate()

	j3.seek(0)
	j3.writelines(cont3)
	j3.truncate()

ori.close()
j2.close()
j3.close()
