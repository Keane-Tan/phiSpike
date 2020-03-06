# -*- coding: utf-8 -*-
import ROOT as rt
import os
import sys
import numpy as np

# Comparing noCut_hadloose_noEDead and noCut_hadloose_mf

dirN = 'phiSpike/NewNormalization/noCut_hadloose_mf'  # directory where the root files are.
dirN_f = 'phiSpike/NewNormalization/noCut_hadloose_noEDead'

tmap = rt.TH2F()
tmap_f = rt.TH2F()

# list directories: ['Data16', 'QCD16', ...]
flist = ['Data16','QCD16','Data17','QCD17','Data18PRE','QCD18PRE','Data18POST','QCD18POST']
varList = ['AK8jet_etaphi_lead','AK8jet_etaphi_sublead','AK4jet_etaphi_lead','AK4jet_etaphi_sublead']

for fl in flist:
	print(fl)

	for var in varList:	
		_file = rt.TFile.Open(dirN+'/'+fl+"/phiSpike.root","READ")
		_file.GetObject(var+"_" + fl,tmap)
		tmap = tmap.Clone(tmap.GetName()+"_")
		tmap.SetDirectory(0)
		_file.Close()

		_file2 = rt.TFile.Open(dirN_f+'/'+fl+"/phiSpike.root","READ")
		_file2.GetObject(var+"_" + fl,tmap_f)
		tmap_f = tmap_f.Clone(tmap_f.GetName()+"_")
		tmap_f.SetDirectory(0)
		_file2.Close()

		c = rt.TCanvas("c", "canvas", 1300, 900)		

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
				zmax = 236.263244629
			if var == "AK8jet_etaphi_sublead":
				zmax = 428.403015137
			if var == "AK4jet_etaphi_lead":
				zmax = 235.639968872
			if var == "AK4jet_etaphi_sublead":
				zmax = 452.341888428
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
				zmax = 111.921333313
			if var == "AK8jet_etaphi_sublead":
				zmax = 622.711669922
			if var == "AK4jet_etaphi_lead":
				zmax = 110.570068359
			if var == "AK4jet_etaphi_sublead":
				zmax = 689.298034668
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
				zmax = 22.7161483765
			if var == "AK8jet_etaphi_sublead":
				zmax = 349.057861328
			if var == "AK4jet_etaphi_lead":
				zmax = 26.6160316467
			if var == "AK4jet_etaphi_sublead":
				zmax = 381.134552002
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
				zmax = 40.172542572
			if var == "AK8jet_etaphi_sublead":
				zmax = 611.86517334
			if var == "AK4jet_etaphi_lead":
				zmax = 47.0873031616
			if var == "AK4jet_etaphi_sublead":
				zmax = 667.858459473

		tmap_norm = rt.TH2F(var,var,50,-2.4,2.4,50,-3.5,3.5)
		tmap_diff = rt.TH2F(var,var,50,-2.4,2.4,50,-3.5,3.5)

		for xi in range(50):
			for yi in range(50):
				v=tmap.GetBinContent(xi,yi)
				vrat = v/zmax
				tmap_norm.SetBinContent(xi,yi,vrat) # normalizing by dividing by the largest z-value

				vf=tmap_f.GetBinContent(xi,yi)
				vfrat = vf/zmax
				tmap_diff.SetBinContent(xi,yi,vfrat) # normalizing by dividing by the largest z-value

		tmap_diff.Add(tmap_norm,-1)
		tmap_diff.GetXaxis().SetTitle("#eta")
		tmap_diff.GetYaxis().SetTitle("#phi")
		#tmap.GetXaxis().SetTitleOffset(1.2)
		tmap_diff.GetYaxis().SetTitleOffset(0.8) 
		tmap_diff.GetZaxis().SetRangeUser(0,1.2) 
		tmap_diff.Draw("colz")

		plotname= dirN + '/'+fl+"/Diff_"+var+".png"
		c.SaveAs(plotname)
