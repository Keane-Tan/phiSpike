# -*- coding: utf-8 -*-
import ROOT as rt
import sys

def norm(hist):
	if hist.Integral(0,hist.GetNbinsX()) > 0:
		hist.Scale(1.0/hist.Integral(0,hist.GetNbinsX())) # normalizing the histograms

def plotHist(bkg,var,year):
	c = rt.TCanvas("c", "canvas", 800, 800) # we will use this for plotting		
	
	stack = rt.THStack()

	hList = [tempHist[bkg+"_hot"],tempHist[bkg+"_nothot"]]
	for histo in hList:
		stack.Add(histo)
	stack.Draw("nostackHIST")
	ymax = stack.GetMaximum()	

	stack.GetXaxis().SetTitle(varList[var+'_hot'][0])
	stack.GetYaxis().SetTitle("Events (Normalized)")
	stack.GetXaxis().SetTitleOffset(1.2)
	stack.GetYaxis().SetTitleOffset(1.4) 
	stack.SetMaximum(ymax*5) 

	rt.gPad.Update()
	rt.gPad.SetLogy(1)

	leg = rt.TLegend(0.6,0.8,0.8,0.89)
	leg.AddEntry(hList[0],'Inside Hotspots', "l")
	leg.AddEntry(hList[1],'Outside of Hotspots', "l")
	leg.SetTextSize(0.03)
	leg.SetBorderSize(0)
	leg.Draw('same')

	plotname= bkg+'_'+var+year+".png"
	c.SaveAs(plotname)


sbL = ['Data', 'QCD']
yearl = ["16"]

tQ_hot = rt.TH1F()
tQ_nothot = rt.TH1F()
tD_hot = rt.TH1F()
tD_nothot = rt.TH1F()

tempHist = {"Data_hot":tQ_hot,"Data_nothot":tQ_nothot,"QCD_hot":tQ_hot,"QCD_nothot":tQ_nothot}

varList = {
	'Jets[1]_muonEnergyFraction_hot':["AK4Jet[1] Muon Energy Fraction"],
	'Jets[1]_electronEnergyFraction_hot':["AK4Jet[1] Electron Energy Fraction"],
	'Jets[1]_photonEnergyFraction_hot':["AK4Jet[1] Photon Energy Fraction"],
	'Jets[1]_neutralHadronEnergyFraction_hot':["AK4Jet[1] Neutral Hadron Energy Fraction"],
	'Jets[1]_chargedHadronEnergyFraction_hot':["AK4Jet[1] Charged Hadron Energy Fraction"],
	'Jets[1]_muonEnergyFraction_nothot':["AK4Jet[1] Muon Energy Fraction"],
	'Jets[1]_electronEnergyFraction_nothot':["AK4Jet[1] Electron Energy Fraction"],
	'Jets[1]_photonEnergyFraction_nothot':["AK4Jet[1] Photon Energy Fraction"],
	'Jets[1]_neutralHadronEnergyFraction_nothot':["AK4Jet[1] Neutral Hadron Energy Fraction"],
	'Jets[1]_chargedHadronEnergyFraction_nothot':["AK4Jet[1] Charged Hadron Energy Fraction"]
}

varSL = ['Jets[1]_muonEnergyFraction','Jets[1]_electronEnergyFraction','Jets[1]_photonEnergyFraction','Jets[1]_neutralHadronEnergyFraction','Jets[1]_chargedHadronEnergyFraction']

ColorDict = {"Data_hot":602,"Data_nothot":801,"QCD_hot":602,"QCD_nothot":801}

for year in yearl:
	for var in varSL:
		print(var)

		for ibkg in range(len(sbL)):
			sb = sbL[ibkg]
			sbName = sb + year
			print "opening file..."
			print sbName + "/phiSpike_with_BEFilter.root"
			_file = rt.TFile.Open(sbName+"/phiSpike_with_BEFilter.root","READ")
			print var+"_"+sbName

			varH = var + '_hot'
			sbH = sb + '_hot'
			_file.GetObject(varH+"_"+sbName,tempHist[sbH])
			tempHist[sbH] = tempHist[sbH].Clone(tempHist[sbH].GetName()+"_")
			tempHist[sbH].SetDirectory(0)
			tempHist[sbH].SetLineColor(ColorDict[sbH])
			tempHist[sbH].SetLineStyle(1)
			norm(tempHist[sbH])
			_file.Close()

			_file = rt.TFile.Open(sbName+"/phiSpike_with_BEFilter.root","READ")
			varN = var + '_nothot'
			sbN = sb + '_nothot'
			_file.GetObject(varN+"_"+sbName,tempHist[sbN])
			tempHist[sbN] = tempHist[sbN].Clone(tempHist[sbN].GetName()+"_")
			tempHist[sbN].SetDirectory(0)
			tempHist[sbN].SetLineColor(ColorDict[sbN])
			tempHist[sbN].SetLineStyle(1)
			norm(tempHist[sbN])
			_file.Close()

		plotHist('Data',var,year)
		plotHist('QCD',var,year)
