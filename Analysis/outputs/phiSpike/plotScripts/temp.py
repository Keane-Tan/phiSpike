import os

#numlist = ['1','1p1','1p2','1p5','2p0','2p5','3p0','5p0','6p0','10p0','15p0','20p0','100p0']
numlist = ['1p5','2p0']

#yearlist = ['16','17','18PRE','18POST']
yearlist = ['17']

# delete all the existing files with the mean distances.
for iy in yearlist:
	distFile = iy + '_meanD.txt'
	if os.path.exists(distFile):
		os.system("rm "+distFile)

for num in numlist:
	# change the k scale in the macro file
	mfilename = "phiSpike_dataMC_Ratios.py"
	mfile = open(mfilename,'r+')

	mf = mfile.readlines()
	mf[199] = "dirN = '../TriggerEff/METScale/phiSpikeFilter/"+num+"' \n" #phiSpikeFilter or noPhiSpike

	mfile.seek(0)
	mfile.writelines(mf)
	mfile.truncate()

	mfile.close()

	os.system("python "+mfilename)
