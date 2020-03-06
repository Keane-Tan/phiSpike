import os

# list of k scale
klist = [1.3,1.4,1.6,1.7]

for kval in klist:
	# make a new directory to save the results
	outputdir = "outputs/phiSpike/TriggerEff/METScale/phiSpikeFilter/" #phiSpikeFilter or noPhiSpike

	outfoldername = outputdir + str(kval).replace(".","p")
	if not os.path.exists(outfoldername):
		os.system("mkdir "+outfoldername)

	# change the weight in the macro file
	mfilename = "macros/datamc/METScale.py"
	mfile = open(mfilename,'r+')

	mf = mfile.readlines()
	mf[146] = "\t\t\tweight = weight * " + str(kval) +"\n"

	mfile.seek(0)
	mfile.writelines(mf)
	mfile.truncate()

	mfile.close()

	# change the output directory in the bash script
	bfilename = "run_DMC.sh"
	bfile = open(bfilename,'r+')

	bf = bfile.readlines()
	bf[11] = 'OUTDIR="'+outfoldername+'/"\n'

	bfile.seek(0)
	bfile.writelines(bf)
	bfile.truncate()

	bfile.close()

	# run the macro
	os.system("./run_DMC.sh METScale")

