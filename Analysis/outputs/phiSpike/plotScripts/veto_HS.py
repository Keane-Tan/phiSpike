# -*- coding: utf-8 -*-
import ROOT as rt
import os
import sys
import numpy as np

# this code extends a radius around the eta and phi values that correspond to hot spots.

dirN = '../TriggerEff/test/rad0p35'  # directory where the root files are.
# list directories: ['Data16', 'QCD16', ...]
#flist = ['Data16','QCD16']
flist = ['Data16','QCD16','Data17','QCD17','Data18PRE','QCD18PRE','Data18POST','QCD18POST']
print flist
tmap = rt.TH2F()

varList = ['AK8jet[0]_etaphi','AK8jet[1]_etaphi','AK4jet[0]_etaphi','AK4jet[1]_etaphi']

selList = [] # contains all the selection filters for Data16, QCD16, ...

sfile = open('Output_Txt/HS_for_LeadingJets.txt','r+')
sfile.truncate(0)

for fl in flist:
	print(fl)

	for var in varList:
		sfile = open('Output_Txt/HS_for_LeadingJets.txt','r+')
		sf = sfile.readlines()	
		_file = rt.TFile.Open(dirN+'/'+fl+"/phiSpike.root","READ")
		print var+"_"+fl
		_file.GetObject(var+"_" + fl,tmap)
		tmap = tmap.Clone(tmap.GetName()+"_")
		tmap.SetDirectory(0)
		_file.Close()	
	
		zmax = tmap.GetBinContent(tmap.GetMaximumBin())

#		Every 2D plots are normalized to the values below
		if fl == "Data16":
			if var == "AK8jet[0]_etaphi":
				zmax = 172.0
			if var == "AK8jet[1]_etaphi":
				zmax = 527.0
			if var == "AK4jet[0]_etaphi":
				zmax = 178.0
			if var == "AK4jet[1]_etaphi":
				zmax = 614.0
		if fl == "QCD16":
			if var == "AK8jet[0]_etaphi":
				zmax = 233.8334198
			if var == "AK8jet[1]_etaphi":
				zmax = 423.674591064
			if var == "AK4jet[0]_etaphi":
				zmax = 233.217590332
			if var == "AK4jet[1]_etaphi":
				zmax = 447.355712891
		if fl == "Data17":
			if var == "AK8jet[0]_etaphi":
				zmax = 231.0
			if var == "AK8jet[1]_etaphi":
				zmax = 589.0
			if var == "AK4jet[0]_etaphi":
				zmax = 244.0
			if var == "AK4jet[1]_etaphi":
				zmax = 697.0
		if fl == "QCD17":
			if var == "AK8jet[0]_etaphi":
				zmax = 109.397438049
			if var == "AK8jet[1]_etaphi":
				zmax = 605.934448242
			if var == "AK4jet[0]_etaphi":
				zmax = 108.07900238
			if var == "AK4jet[1]_etaphi":
				zmax = 670.706176758
		if fl == "Data18PRE":
			if var == "AK8jet[0]_etaphi":
				zmax = 47.0
			if var == "AK8jet[1]_etaphi":
				zmax = 294.0
			if var == "AK4jet[0]_etaphi":
				zmax = 52.0
			if var == "AK4jet[1]_etaphi":
				zmax = 326.0
		if fl == "QCD18PRE":
			if var == "AK8jet[0]_etaphi":
				zmax = 21.9174785614
			if var == "AK8jet[1]_etaphi":
				zmax = 338.850036621
			if var == "AK4jet[0]_etaphi":
				zmax = 25.6687889099
			if var == "AK4jet[1]_etaphi":
				zmax = 370.0809021
		if fl == "Data18POST":
			if var == "AK8jet[0]_etaphi":
				zmax = 82.0
			if var == "AK8jet[1]_etaphi":
				zmax = 602.0
			if var == "AK4jet[0]_etaphi":
				zmax = 87.0
			if var == "AK4jet[1]_etaphi":
				zmax = 679.0
		if fl == "QCD18POST":
			if var == "AK8jet[0]_etaphi":
				zmax = 38.7591094971
			if var == "AK8jet[1]_etaphi":
				zmax = 593.931030273
			if var == "AK4jet[0]_etaphi":
				zmax = 45.4079933167
			if var == "AK4jet[1]_etaphi":
				zmax = 648.458496094

		tmap_norm = rt.TH2F(var,var,50,-2.4,2.4,50,-3.5,3.5)
		mapVal = rt.TH1F(var,var,50,0,1)
		etaHist = rt.TH1F(var,var,50,-2.4,2.4) # etaHist and phiHist are defined here for getting the low bin edges. I don't know how to do that 
		phiHist = rt.TH1F(var,var,50,-3.5,3.5) # with 2D histograms.

		selecV = [] # selection criteria to get rid of phi spikes
		for xi in range(50):
			for yi in range(50):
				v=tmap.GetBinContent(xi,yi)
				vrat = v/zmax
				tmap_norm.SetBinContent(xi,yi,vrat) # normalizing by dividing by the largest z-value
				if vrat > 1:
					vrat = 1
				mapVal.Fill(vrat*0.99)

				# Identifying the eta and phi ranges with unusually high number of events
				ed = round(etaHist.GetBinWidth(xi),3)
				etaP = round(etaHist.GetBinCenter(xi),3)
				pd = round(phiHist.GetBinWidth(yi),3)
				phiP = round(phiHist.GetBinCenter(yi),3)

				crit = str(etaP) + "," + str(phiP)

				if var == "AK4jet[0]_etaphi":
					if "Data16" in fl and vrat > 0.2:       # 0.34 for AK4jet[1]_etaphi
						selecV.append(crit)

					if "QCD16" in fl and vrat > 0.2:	# 0.31 forjet[1]
						selecV.append(crit)

					if "Data17" in fl and vrat > 0.2:	# 0.46 forjet[1]
						selecV.append(crit)

					if "QCD17" in fl and vrat > 0.2:	# 0.29 forjet[1]
						selecV.append(crit)

					if "Data18PRE" in fl and vrat > 0.7:	# 0.29 forjet[1]
						selecV.append(crit)

					if "QCD18PRE" in fl and vrat > 0.98:	# 0.23 forjet[1]
						selecV.append("NA")

					if "Data18POST" in fl and vrat > 0.7:	# 0.36 forjet[1]
						selecV.append(crit)

					if "QCD18POST" in fl and vrat > 0.98:	# 0.23 forjet[1]
						selecV.append("NA")

		if len(selecV) > 0:
			selList.append(selecV)

# this part only works when the conditional statements in the previous section are written in the order above: QCD16, Data16, etc.
for isl in range(len(selList)): 
	if isl*2 < len(selList) - 1:
		a = selList[isl*2]
		b = selList[isl*2+1]
		# making sure that the same conditions are not repeated for the same year
		for elem in b:
			if elem not in a:
				a.append(elem)

		# Get the conditional statement to veto events with eta and phi values that cause phi spike.
		# save the conditional statement to etaPhiSelec.txt			
		etaC = "["
		phiC = "["

		for si in range(len(a)):
			sep = a[si].find(",") # find the index of the comma that separates the eta and phi values
			eta_v = a[si][:sep]
			phi_v = a[si][sep+1:]

			if si == len(a)-1:
				etaC = etaC + eta_v + "]"
				phiC = phiC + phi_v + "]"
			else:
				etaC = etaC + eta_v + ","
				phiC = phiC + phi_v + ","
		
		sf.append(etaC + "\n")
		sf.append(phiC + "\n\n")
		sfile.seek(0) 	# this together with .truncate() allows us to overwrite the text file
		sfile.writelines(sf)
		sfile.truncate()

sfile.close()


