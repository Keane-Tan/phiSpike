# -*- coding: utf-8 -*-
import ROOT as rt
import os
import sys
import numpy as np

# this code extends a radius around the eta and phi values that correspond to hot spots.

dirN = '../TriggerEff/OccupancyPlots/Leading'  # directory where the root files are.
# list directories: ['Data16', 'QCD16', ...]
#flist = ['Data16','QCD16']
flist = ['Data16','QCD16','Data17','QCD17','Data18PRE','QCD18PRE','Data18POST','QCD18POST']
print flist
tmap = rt.TH2F()

varList = ['AK8jet[0]_etaphi','AK8jet[1]_etaphi','AK4jet[0]_etaphi','AK4jet[1]_etaphi']

for fl in flist:
	print(fl)

	for var in varList:
		_file = rt.TFile.Open(dirN+'/'+fl+"/phiSpikeOcc.root","READ")
		#_file = rt.TFile.Open(dirN+'/'+fl+"/phiSpike_with_BEFilter.root","READ")
		print var+"_"+fl
		_file.GetObject(var+"_" + fl,tmap)
		tmap = tmap.Clone(tmap.GetName()+"_")
		tmap.SetDirectory(0)
		_file.Close()

		rt.gStyle.SetOptTitle(1)
		rt.gStyle.SetOptStat(0)  # gets rid of the default legend with statistical information
		c = rt.TCanvas("c", "canvas", 1300, 900)	
		c.SetRightMargin(0.2)

#		Every 2D plots are normalized to the values below
		if fl == "Data16":
			if var == "AK8jet[0]_etaphi":
				zmax = 172.0
			if var == "AK8jet[1]_etaphi":
				zmax = 527.0
			if var == "AK8jet[2]_etaphi":
				zmax = 28.0
			if var == "AK8jet[3]_etaphi":
				zmax = 4.0
			if var == "AK4jet[0]_etaphi":
				zmax = 178.0
			if var == "AK4jet[1]_etaphi":
				zmax = 614.0
			if var == "AK4jet[2]_etaphi":
				zmax = 47.0
			if var == "AK4jet[3]_etaphi":
				zmax = 30.0
		if fl == "QCD16":
			if var == "AK8jet[0]_etaphi":
				zmax = 233.8334198
			if var == "AK8jet[1]_etaphi":
				zmax = 423.674591064
			if var == "AK8jet[2]_etaphi":
				zmax = 30.3885364532
			if var == "AK8jet[3]_etaphi":
				zmax = 13.3354139328
			if var == "AK4jet[0]_etaphi":
				zmax = 233.217590332
			if var == "AK4jet[1]_etaphi":
				zmax = 447.355712891
			if var == "AK4jet[2]_etaphi":
				zmax = 232.027633667
			if var == "AK4jet[3]_etaphi":
				zmax = 28.4290790558
		if fl == "Data17":
			if var == "AK8jet[0]_etaphi":
				zmax = 231.0
			if var == "AK8jet[1]_etaphi":
				zmax = 589.0
			if var == "AK8jet[2]_etaphi":
				zmax = 42.0
			if var == "AK8jet[3]_etaphi":
				zmax = 5.0
			if var == "AK4jet[0]_etaphi":
				zmax = 244.0
			if var == "AK4jet[1]_etaphi":
				zmax = 697.0
			if var == "AK4jet[2]_etaphi":
				zmax = 78.0
			if var == "AK4jet[3]_etaphi":
				zmax = 32.0
		if fl == "QCD17":
			if var == "AK8jet[0]_etaphi":
				zmax = 109.397438049
			if var == "AK8jet[1]_etaphi":
				zmax = 605.934448242
			if var == "AK8jet[2]_etaphi":
				zmax = 23.4741764069
			if var == "AK8jet[3]_etaphi":
				zmax = 4.283162117
			if var == "AK4jet[0]_etaphi":
				zmax = 108.07900238
			if var == "AK4jet[1]_etaphi":
				zmax = 670.706176758
			if var == "AK4jet[2]_etaphi":
				zmax = 111.244697571
			if var == "AK4jet[3]_etaphi":
				zmax = 15.95408535
		if fl == "Data18PRE":
			if var == "AK8jet[0]_etaphi":
				zmax = 47.0
			if var == "AK8jet[1]_etaphi":
				zmax = 294.0
			if var == "AK8jet[2]_etaphi":
				zmax = 18.0
			if var == "AK8jet[3]_etaphi":
				zmax = 4.0
			if var == "AK4jet[0]_etaphi":
				zmax = 52.0
			if var == "AK4jet[1]_etaphi":
				zmax = 326.0
			if var == "AK4jet[2]_etaphi":
				zmax = 36.0
			if var == "AK4jet[3]_etaphi":
				zmax = 19.0
		if fl == "QCD18PRE":
			if var == "AK8jet[0]_etaphi":
				zmax = 21.9174785614
			if var == "AK8jet[1]_etaphi":
				zmax = 338.850036621
			if var == "AK8jet[2]_etaphi":
				zmax = 15.5412015915
			if var == "AK8jet[3]_etaphi":
				zmax = 5.09862232208
			if var == "AK4jet[0]_etaphi":
				zmax = 25.6687889099
			if var == "AK4jet[1]_etaphi":
				zmax = 370.0809021
			if var == "AK4jet[2]_etaphi":
				zmax = 23.3281745911
			if var == "AK4jet[3]_etaphi":
				zmax = 12.38971138
		if fl == "Data18POST":
			if var == "AK8jet[0]_etaphi":
				zmax = 82.0
			if var == "AK8jet[1]_etaphi":
				zmax = 602.0
			if var == "AK8jet[2]_etaphi":
				zmax = 29.0
			if var == "AK8jet[3]_etaphi":
				zmax = 5.0
			if var == "AK4jet[0]_etaphi":
				zmax = 87.0
			if var == "AK4jet[1]_etaphi":
				zmax = 679.0
			if var == "AK4jet[2]_etaphi":
				zmax = 61.0
			if var == "AK4jet[3]_etaphi":
				zmax = 28.0
		if fl == "QCD18POST":
			if var == "AK8jet[0]_etaphi":
				zmax = 38.7591094971
			if var == "AK8jet[1]_etaphi":
				zmax = 593.931030273
			if var == "AK8jet[2]_etaphi":
				zmax = 25.451669693
			if var == "AK8jet[3]_etaphi":
				zmax = 9.3451089859
			if var == "AK4jet[0]_etaphi":
				zmax = 45.4079933167
			if var == "AK4jet[1]_etaphi":
				zmax = 648.458496094
			if var == "AK4jet[2]_etaphi":
				zmax = 40.0134658813
			if var == "AK4jet[3]_etaphi":
				zmax = 22.7072582245
		if var == "AK8jet[0]_etaphi":
			varname = "AK8jet[1]_etaphi"
		if var == "AK8jet[1]_etaphi":
			varname = "AK8jet[2]_etaphi"
		if var == "AK4jet[0]_etaphi":
			varname = "AK4jet[1]_etaphi"
		if var == "AK4jet[1]_etaphi":
			varname = "AK4jet[2]_etaphi"


		tmap_norm = rt.TH2F(fl+"_"+varname,fl+"_"+varname,50,-2.4,2.4,50,-3.5,3.5)
		mapVal = rt.TH1F(fl+"_"+var[:-7],fl+"_"+var[:-7],50,0,1)

		for xi in range(50):
			for yi in range(50):
				v=tmap.GetBinContent(xi,yi)
				vrat = v/zmax
				tmap_norm.SetBinContent(xi,yi,vrat) # normalizing by dividing by the largest z-value
				if vrat > 1:
					vrat = 1
				mapVal.Fill(vrat*0.99)

		if var == "AK8jet[0]_etaphi":
			titlename = fl+"_AK8jet[1]_etaphi"
		if var == "AK8jet[1]_etaphi":
			titlename = fl+"_AK8jet[2]_etaphi"
		if var == "AK4jet[0]_etaphi":
			titlename = fl+"_AK4jet[1]_etaphi"
		if var == "AK4jet[1]_etaphi":
			titlename = fl+"_AK4jet[2]_etaphi"

		tmap_norm.Draw("colz")
		tmap_norm.SetTitle(titlename)
		tmap_norm.GetXaxis().SetTitle("#eta")
		tmap_norm.GetXaxis().SetTitleSize(80)
		tmap_norm.GetXaxis().SetTitleFont(43)
		tmap_norm.GetXaxis().SetTitleOffset(0.3)

		tmap_norm.GetYaxis().SetTitle("#phi")
		tmap_norm.GetYaxis().SetTitleSize(80)
		tmap_norm.GetYaxis().SetTitleFont(43)
		tmap_norm.GetYaxis().SetTitleOffset(0.3) 

		tmap_norm.GetZaxis().SetTitle("Fraction of Events")
		tmap_norm.GetZaxis().SetTitleSize(60)
		tmap_norm.GetZaxis().SetTitleFont(43)
		tmap_norm.GetZaxis().SetTitleOffset(0.6) 
		tmap_norm.GetZaxis().SetRangeUser(0,1.2) 

		mapVal.SetTitle(titlename)
		mapVal.GetXaxis().SetTitle("Fraction of Events")
		mapVal.GetYaxis().SetTitle("Number of Bins")
		mapVal.GetXaxis().SetTitleOffset(1.2)
		mapVal.GetYaxis().SetTitleOffset(1.4) 

		plotname= dirN + '/'+fl+"/"+var+".pdf"
		c.Update()
		c.SaveAs(plotname)

		c2 = rt.TCanvas("c2", "canvas", 800, 800)

		mapVal.Draw()
		# Vertical line to indicate how we decide the hot spots
		ymax = mapVal.GetMaximum()
		if var == 'AK4jet[1]_etaphi':
			if "Data16" in fl:
				cutX = 0.34
			if "QCD16" in fl:
				cutX = 0.31
			if "Data17" in fl:
				cutX = 0.46
			if "QCD17" in fl:
				cutX = 0.29
			if "Data18PRE" in fl:
				cutX = 0.29
			if "QCD18PRE" in fl:
				cutX = 0.23
			if "Data18POST" in fl:
				cutX = 0.36
			if "QCD18POST" in fl:
				cutX = 0.23

			line = rt.TLine(cutX,0,cutX,ymax)
			line.SetLineColor(rt.kRed)
			line.SetLineWidth(6)
			line.SetLineStyle(2)
			line.Draw("same")

		if var == 'AK4jet[0]_etaphi':
			if "Data16" in fl:
				cutX = 0.43
			if "QCD16" in fl:
				cutX = 0.9
			if "Data17" in fl:
				cutX = 0.41
			if "QCD17" in fl:
				cutX = 0.9
			if "Data18PRE" in fl:
				cutX = 0.7
			if "QCD18PRE" in fl:
				cutX = 0.98
			if "Data18POST" in fl:
				cutX = 0.7
			if "QCD18POST" in fl:
				cutX = 0.98

			line = rt.TLine(cutX,0,cutX,ymax)
			line.SetLineColor(rt.kRed)
			line.SetLineWidth(6)
			line.SetLineStyle(2)
			line.Draw("same")

		c2.SetLogy()
		c2.SaveAs(dirN + '/'+fl+"/"+'1D_mapValues'+var+'.pdf')

