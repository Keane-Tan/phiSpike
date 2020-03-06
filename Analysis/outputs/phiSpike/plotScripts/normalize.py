# -*- coding: utf-8 -*-
import ROOT as rt
import os
import sys
import numpy as np

# this code extends a radius around the eta and phi values that correspond to hot spots.

dirN = '../TriggerEff/noCut_mf'  # directory where the root files are.
# list directories: ['Data16', 'QCD16', ...]
flist = ['Data16','QCD16','Data17','QCD17','Data18PRE','QCD18PRE','Data18POST','QCD18POST']

tmap = rt.TH2F()

varList = ['AK8jet[0]_etaphi','AK8jet[1]_etaphi','AK8jet[2]_etaphi','AK8jet[3]_etaphi','AK4jet[0]_etaphi','AK4jet[1]_etaphi','AK4jet[2]_etaphi','AK4jet[3]_etaphi']

nfile_dir = 'Output_Txt/NormalizationValues.txt'
nfile = open(nfile_dir,'r+')
nfile.truncate(0)
normList = []


print("Start calculating normalization values using mf files...")

for fl in flist:
	for var in varList:
		_file = rt.TFile.Open(dirN+'/'+fl+"/phiSpike.root","READ")
		_file.GetObject(var+"_" + fl,tmap)
		tmap = tmap.Clone(tmap.GetName()+"_")
		tmap.SetDirectory(0)
		_file.Close()		
	
		zmax = tmap.GetBinContent(tmap.GetMaximumBin())
	
		## saving values for normalization to normList
		fln = 'if fl == "' + fl + '":\n'
		varn = '\tif var == "' + var + '":\n'
		zmaxn = '\t\tzmax = ' + str(zmax) + '\n'
		if var == "AK8jet[0]_etaphi":
			normList.append(fln)
		normList.append(varn)
		normList.append(str(zmaxn))

print("Finish calculating normalization values using mf files.")
print("See results at " + nfile_dir)

## saving values for the text file
nfile.seek(0)
nfile.writelines(normList)
nfile.truncate()
nfile.close()
