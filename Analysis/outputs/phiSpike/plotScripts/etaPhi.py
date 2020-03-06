# -*- coding: utf-8 -*-
import ROOT as rt
import os
import sys
import numpy as np

def norm(hist):
	if hist.Integral(0,hist.GetNbinsX()) > 0:
		hist.Scale(1.0/hist.Integral(0,hist.GetNbinsX())) # normalizing the histograms


dirN = 'phiSpike/TriggerEff/noCut'  # directory where the root files are.

flist = ['Data16','QCD16','Data17','QCD17','Data18PRE','QCD18PRE','Data18POST','QCD18POST']
print flist
tmap = rt.TH2F()

varList = ['AK8jet_etaphi_lead','AK8jet_etaphi_sublead','AK4jet_etaphi_lead','AK4jet_etaphi_sublead']

selList = [] # contains all the selection filters for Data16, QCD16, ...

sfile = open('etaPhiSelec.txt','r+')
sfile.truncate(0)

## Uncomment these and some of the lines below only if want to save normalization values.
#nfile = open('phiSpike/NormalizationValues.txt','r+')
#nfile.truncate(0)
#normList = []

for fl in flist:
	print(fl)

	for var in varList:
		sfile = open('etaPhiSelec.txt','r+')
		sf = sfile.readlines()	
		_file = rt.TFile.Open(dirN+'/'+fl+"/phiSpike.root","READ")
		print var+"_"+fl
		_file.GetObject(var+"_" + fl,tmap)
		tmap = tmap.Clone(tmap.GetName()+"_")
		tmap.SetDirectory(0)
		#norm(tmap)
		_file.Close()

		c = rt.TCanvas("c", "canvas", 1300, 900)		
	
		zmax = tmap.GetBinContent(tmap.GetMaximumBin())
	
		## saving values for normalization to normList
#		fln = 'if fl == "' + fl + '":\n'
#		varn = '\tif var == "' + var + '":\n'
#		zmaxn = '\t\tzmax = ' + str(zmax) + '\n'
#		if var == "AK8jet_etaphi_lead":
#			normList.append(fln)
#		normList.append(varn)
#		normList.append(str(zmaxn))

#		Every 2D plots are normalized to the values below

		if fl == "Data16":
			if var == "AK8jet_etaphi_lead":
				zmax = 172.0
			if var == "AK8jet_etaphi_sublead":
				zmax = 527.0
			if var == "AK4jet_etaphi_lead":
				zmax = 178.0
			if var == "AK4jet_etaphi_sublead":
				zmax = 614.0
		if fl == "QCD16":
			if var == "AK8jet_etaphi_lead":
				zmax = 233.8334198
			if var == "AK8jet_etaphi_sublead":
				zmax = 423.674591064
			if var == "AK4jet_etaphi_lead":
				zmax = 233.217590332
			if var == "AK4jet_etaphi_sublead":
				zmax = 447.355712891
		if fl == "Data17":
			if var == "AK8jet_etaphi_lead":
				zmax = 231.0
			if var == "AK8jet_etaphi_sublead":
				zmax = 589.0
			if var == "AK4jet_etaphi_lead":
				zmax = 244.0
			if var == "AK4jet_etaphi_sublead":
				zmax = 697.0
		if fl == "QCD17":
			if var == "AK8jet_etaphi_lead":
				zmax = 109.397438049
			if var == "AK8jet_etaphi_sublead":
				zmax = 605.934448242
			if var == "AK4jet_etaphi_lead":
				zmax = 108.07900238
			if var == "AK4jet_etaphi_sublead":
				zmax = 670.706176758
		if fl == "Data18PRE":
			if var == "AK8jet_etaphi_lead":
				zmax = 47.0
			if var == "AK8jet_etaphi_sublead":
				zmax = 294.0
			if var == "AK4jet_etaphi_lead":
				zmax = 52.0
			if var == "AK4jet_etaphi_sublead":
				zmax = 326.0
		if fl == "QCD18PRE":
			if var == "AK8jet_etaphi_lead":
				zmax = 21.9174785614
			if var == "AK8jet_etaphi_sublead":
				zmax = 338.850036621
			if var == "AK4jet_etaphi_lead":
				zmax = 25.6687889099
			if var == "AK4jet_etaphi_sublead":
				zmax = 370.0809021
		if fl == "Data18POST":
			if var == "AK8jet_etaphi_lead":
				zmax = 82.0
			if var == "AK8jet_etaphi_sublead":
				zmax = 602.0
			if var == "AK4jet_etaphi_lead":
				zmax = 87.0
			if var == "AK4jet_etaphi_sublead":
				zmax = 679.0
		if fl == "QCD18POST":
			if var == "AK8jet_etaphi_lead":
				zmax = 38.7591094971
			if var == "AK8jet_etaphi_sublead":
				zmax = 593.931030273
			if var == "AK4jet_etaphi_lead":
				zmax = 45.4079933167
			if var == "AK4jet_etaphi_sublead":
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
				etawd = round(etaHist.GetBinWidth(xi),3)
				etaLow = round(etaHist.GetBinLowEdge(xi),3)
				etaHigh = round(etaLow + etawd,3)
				phiwd = round(phiHist.GetBinWidth(yi),3)
				phiLow = round(phiHist.GetBinLowEdge(yi),3)
				phiHigh = round(phiLow + phiwd,3)

				crit = str(etaLow) + "<Jets[1].Eta()<" + str(etaHigh) + " and " + str(phiLow) + "<Jets[1].Phi()<" + str(phiHigh)

				if var == "AK4jet_etaphi_sublead":
					if "Data16" in fl and vrat > 0.34:
						selecV.append(crit)

					if "QCD16" in fl and vrat > 0.31:
						selecV.append(crit)

					if "Data17" in fl and vrat > 0.46:
						selecV.append(crit)

					if "QCD17" in fl and vrat > 0.29:
						selecV.append(crit)

					if "Data18PRE" in fl and vrat > 0.29:
						selecV.append(crit)

					if "QCD18PRE" in fl and vrat > 0.23:
						selecV.append(crit)

					if "Data18POST" in fl and vrat > 0.36:
						selecV.append(crit)

					if "QCD18POST" in fl and vrat > 0.23:
						selecV.append(crit)


		if len(selecV) > 0:
			selList.append(selecV)
		tmap_norm.GetXaxis().SetTitle("#eta")
		tmap_norm.GetYaxis().SetTitle("#phi")
		#tmap.GetXaxis().SetTitleOffset(1.2)
		tmap_norm.GetYaxis().SetTitleOffset(0.8) 
		tmap_norm.GetZaxis().SetRangeUser(0,1.2) 
		tmap_norm.Draw("colz")

		mapVal.GetXaxis().SetTitle("Map Values")
		mapVal.GetYaxis().SetTitle("Events")
		mapVal.GetXaxis().SetTitleOffset(1.2)
		mapVal.GetYaxis().SetTitleOffset(1.4) 

		plotname= dirN + '/'+fl+"/"+var+".png"
		c.SaveAs(plotname)

		c2 = rt.TCanvas("c2", "canvas", 800, 800)
		mapVal.Draw()
		c2.SetLogy()
		c2.SaveAs(dirN + '/'+fl+"/"+'1D_mapValues'+var+'.png')

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
		cond = 'if'
		for si in range(len(a)):
			if si == len(a) - 1:
				cond = cond + ' (' + a[si] + '):'
			else:
				cond = cond + ' (' + a[si] + ') or'

		sf.append(cond + "\n\n")
		sfile.seek(0) 	# this together with .truncate() allows us to overwrite the text file
		sfile.writelines(sf)
		sfile.truncate()

## saving values for the text file
#nfile.seek(0)
#nfile.writelines(normList)
#nfile.truncate()
#nfile.close()

sfile.close()


