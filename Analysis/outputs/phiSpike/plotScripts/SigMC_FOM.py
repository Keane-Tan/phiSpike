# -*- coding: utf-8 -*-
import ROOT as rt
import numpy as np

# Comparing noCut_hadloose_noEDead and noCut_hadloose_mf

dirN = '../TriggerEff/SigBkg_Sens/OldCode'  # directory where the root files are.

# list directories: ['Data16', 'QCD16', ...]
flist = ['QCD','TTJets','WJets','ZJets']
#flist = ['QCD']
yearlist = ['16','17','18PRE','18POST']
#yearlist = ['16']

# List of radii for the phi spike filter
rad = 0.028816 		# diagonal of the rectangular eta-phi block
radList = np.linspace(rad*0.05,rad*1.2, 24)

for year in yearlist:
	print year

	# List of total background yields for all the different radii.
	BL = np.zeros(24)
	
	for MC in flist:	
		fl = MC + year
		_file = rt.TFile.Open(dirN+'/'+fl+"/phiSigB.root","READ")
		tr = _file.Get("rtree")

		numberOfEntries = tr.GetEntries()
		print numberOfEntries
		for entry in range(numberOfEntries):
			tr.GetEvent(entry)

			if year == "16":
				dist_br = tr.Dist_to_HS_16
			if year == "17":
				dist_br = tr.Dist_to_HS_17
			if year == "18PRE":
				dist_br = tr.Dist_to_HS_18PRE
			if year == "18POST":
				dist_br = tr.Dist_to_HS_18POST

			nE = tr.Event_Weight

			for ij in range(len(radList)):
				if dist_br >= radList[ij]:
					BL[ij] += nE

	# List of baseline signal yields for all the different radii
	SL = np.zeros(24)

	sfile = rt.TFile.Open(dirN+'/base/phiSigB.root',"READ")
	tr_sig = sfile.Get("rtree")

	numberOfEntries_sig = tr_sig.GetEntries()
	print numberOfEntries_sig

	for sigi in range(numberOfEntries_sig):
		tr_sig.GetEvent(sigi)

		if year == "16":
			dist_sig = tr_sig.Dist_to_HS_16
		if year == "17":
			dist_sig = tr_sig.Dist_to_HS_17
		if year == "18PRE":
			dist_sig = tr_sig.Dist_to_HS_18PRE
		if year == "18POST":
			dist_sig = tr_sig.Dist_to_HS_18POST

		for ik in range(len(radList)):
			if dist_sig >= radList[ik]:
				SL[ik] += 1
	
	print BL
	print SL
	FOM = np.sqrt(2*( (SL +BL) * np.log(1 + SL/BL) - SL ))
	print("The FOM for 20"+year+" are")
	print FOM
