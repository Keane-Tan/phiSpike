import ROOT as rt
import numpy as np
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()

rt.gROOT.SetBatch(True)


def meanRatio(datahist,rathist):
	binNum = datahist.GetNbinsX()
	rat_c = []
	for i in range(binNum):
		if datahist.GetBinContent(i) >= 15:
			rat_c.append(rathist.GetBinContent(i))
	rat_c = np.array(rat_c)

	ratio_mean = np.mean(rat_c)

	meanD = np.mean((rat_c - ratio_mean)**2)

	#print meanD

	return [ratio_mean,meanD]
	
def saveMeanD(mDist,DfileName):
	Dfile = open(DfileName,'a+')
	Dfile.write(str(mDist)+'\n')
	Dfile.close()

def makeRatioBkgStack(bkgList, data, signal, title, xlabel, ylabel, name, doLeg = True, log = False):
	# bkgList is list of bkgHistos
	# data should be a TH1 of data
	# title is the histogram title
	# xlabel is histogram's x axis title
	# ylabel is histogram's y axis title
	# name is what the .png file will be named.

	# Define the Canvas
#	c = rt.TCanvas("c", "canvas", 800, 800)

	H=600
	W=700

	H_ref = 600
	W_ref = 700

	T = 0.08*H_ref
	B = 0.12*H_ref
	L = 0.12*W_ref
	R = 0.08*W_ref

	c = rt.TCanvas("c","canvas",50,50,W,H)
	c.SetFillColor(0);
	c.SetBorderMode(0);
	c.SetFrameFillStyle(0);
	c.SetFrameBorderMode(0);
	c.SetLeftMargin( 0.15 );#L/W                                                                                                                                     
	c.SetRightMargin( R/W );
	c.SetTopMargin( T/H );
	c.SetBottomMargin(0.2);
	c.SetTickx(0);
	c.SetTicky(0);
	c.Draw()

	# define stack of bkgHistos
	stack = rt.THStack()
	for histo in bkgList:
		stack.Add(histo)
	# Upper plot will be in pad1
	pad1 = rt.TPad("pad1", "pad1", 0, 0.3, 0.95, 0.95)
	pad1.SetBottomMargin(0) # Upper and lower plot are joined
	#pad1.SetGridx()         # Vertical grid
	#pad1.SetGridy()         # Horizontal grid
	if log:
		pad1.SetLogy()
	pad1.Draw()             # Draw the upper pad: pad1
	pad1.cd()               # pad1 becomes the current pad
	#stack.SetStats(0)       # No statistics on upper plot
	#data.SetStats(0)       # No statistics on upper plot
	stack.SetMinimum(0.1)
	stack.SetMaximum(100000000)
	stack.Draw("hist")  
	data.Draw("E1 same")
	signal.Draw("same")

	stack.GetYaxis().SetTitle(ylabel)
	stack.GetYaxis().SetTitleSize(30)
	stack.GetYaxis().SetTitleFont(43)
	stack.GetYaxis().SetTitleOffset(1.35)
	stack.GetYaxis().SetLabelFont(43)
	stack.GetYaxis().SetLabelSize(25)

	if doLeg:
#		if (("deltaR" in xlabel) or ("Eta" in xlabel) or ("ptD" in xlabel) or ("BvsAll" in xlabel) or ("ecf" in xlabel) or ("chgH" in xlabel)):
#			leg = rt.TLegend(0.3,0.0,0.7,0.3,title,"brNDC") # pos bot mid
#		else:		
#			leg = rt.TLegend(0.6,0.67,0.85,0.89,title,"brNDC") # pos top right
		leg = rt.TLegend(0.2,0.67,0.9,0.89)
		leg.SetNColumns(3)
#		leg.AddEntry(0,"","")
		for hist in bkgList[::-1]:
			histID = hist.GetName()
			if "QCD" in histID:
				histID = "QCD"
				leg.AddEntry(hist, histID, "f" )
			elif "TTJets" in histID:
				histID = "TTJets"
				leg.AddEntry(hist, histID, "f" )

		leg.AddEntry(data,"Data","EP")
		for hist in bkgList[::-1]:
			histID = hist.GetName()
			if "WJets" in histID:
				histID = "WJets"
				leg.AddEntry(hist, histID, "f" )
			elif "ZJets" in histID:
				histID = "ZJets"
				leg.AddEntry(hist, histID, "f" )
		leg.AddEntry(signal,"SVJ_3000_20_0.3_peak","l")
		ks = stack.GetStack().Last().KolmogorovTest(data)
		chi2 = stack.GetStack().Last().Chi2Test(data,"CHI2/NDF")
		leg.SetTextSize(.06)
		leg.SetTextFont(42)
		leg.SetBorderSize(0)
		leg.Draw()
#		if '#phi' in title:
#			ptext = rt.TPaveText(-1.5,3500,-1.5,4000)
#		else:
#			ptext = rt.TPaveText(1600,100,1600,200)
#		ptext.AddText("KS = {:.2f}, #chi^2/ndf = {:.2f}".format(ks, chi2))
#		ptext.SetTextSize(.04)
#		ptext.SetBorderSize(0)
#		ptext.Draw()
	if data.GetNbinsX() == 100:
		for thing in stack.GetStack():
			thing.Rebin(2)
		data.Rebin(2)

	# Do not draw the Y axis label on the upper plot and redraw a small
	# axis instead, in order to avoid the first label (0) to be clipped.
	#h1.GetYaxis().SetLabelSize(0.)
	#axis = rt.TGaxis( -5, 20, -5, 220, 20,220,510,"")
	#axis.SetLabelFont(43) # Absolute font size in pixel (precision 3)
	#axis.SetLabelSize(15)
	#axis.Draw()

	# lower plot will be in pad2
	c.cd()          # Go back to the main canvas before defining pad2
	pad2 = rt.TPad("pad2", "pad2", 0, 0, 0.95, 0.3)
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.5)
	#pad2.SetGridx() # vertical grid
	#pad2.SetGridy()         # Horizontal grid
	pad2.Draw()
	pad2.cd()       # pad2 becomes the current pad

	# Define the ratio plot
	totBkg = stack.GetStack().Last()
	h3 = data.Clone("h3")
	h3.SetLineColor(rt.kBlack)
	h3.SetMinimum(0.0)  # Define Y ..
	h3.SetMaximum(1.8) # .. range
	h3.Sumw2()
	h3.SetStats(0)      # No statistics on lower plot
	h3.Divide(totBkg)
	h3.SetMarkerStyle(21)
	h3.Draw("ep")       # Draw the ratio plot

	# data settings
	data.SetMarkerColor(rt.kBlack)

	# Y axis h1 plot settings
	data.GetYaxis().SetTitleSize(30)
	data.GetYaxis().SetTitleFont(43)
	data.GetYaxis().SetTitleOffset(1.88)

	# Ratio plot (h3) settings
	data.SetTitle("") # Remove the ratio title
	h3.SetTitle("") # Remove the ratio title

	# Y axis ratio plot settings
	h3.GetYaxis().SetTitle("Data/Bkg")
	h3.GetYaxis().SetNdivisions(505)
	h3.GetYaxis().SetTitleSize(30)
	h3.GetYaxis().SetTitleFont(43)
	h3.GetYaxis().SetTitleOffset(1.1)
	h3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
	h3.GetYaxis().SetLabelSize(25)

	# X axis ratio plot settings
	h3.GetXaxis().SetTitle(xlabel)
	h3.GetXaxis().SetTitleSize(33)
	h3.GetXaxis().SetTitleFont(43)
	h3.GetXaxis().SetTitleOffset(3.2)
	h3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
	h3.GetXaxis().SetLabelSize(25)

	pad1.Update()
	pad2.Update()
	c.Update()
	const = rt.TF1("const", '[0]', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
	line = rt.TF1("line", '[0]+[1]*x', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
	one = rt.TF1("one", '1', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
	one.SetLineStyle(2)
	#h3.Fit("const","Q")
	one.SetLineColor(rt.kBlack)
	one.Draw("same")

	# Draw the mean ratio line
	mRatio = meanRatio(data,h3)[0]
	mLine = rt.TLine(h3.GetXaxis().GetXmin(),mRatio,h3.GetXaxis().GetXmax(),mRatio)
	mLine.SetLineColor(rt.kBlue)
	mLine.SetLineWidth(3)
	mLine.SetLineStyle(2)
#	mLine.Draw("same")

#	leg2 = rt.TLegend(0.2,0.8,0.6,0.95) 
#	leg2.AddEntry(mLine,"mean ratio = "+str(round(mRatio,3)),"l")
#	leg2.Draw('same')

	# Save the mean distance
	if '16' in title:
		DfileName = '16'
	elif '17' in title:
		DfileName = '17'
	elif '18PRE' in title:
		DfileName = '18PRE'
	elif '18POST' in title:
		DfileName = '18POST'
	else:
		DfileName = 'DoesNotExist'

	saveMeanD(meanRatio(data,h3)[1],DfileName+'_meanD.txt')

	# CMS Label
	CMS_lumi.writeExtraText = 0

	if '16' in title:
		lumi = '35.9'
	elif '17' in title:
		lumi = '41.5'
	elif '18PRE' in title:
		lumi = '21.1'
	elif '18POST' in title:
		lumi = '38.6'

	CMS_lumi.lumi_sqrtS = lumi + " fb^{-1} (13 TeV)"

	iPeriod = 0
	iPos = 1

	CMS_lumi.CMS_lumi(c, iPeriod, iPos)
	c.cd()
	c.Update();
	c.RedrawAxis()
	
	#save as .png
	c.SaveAs(name)
	c.Delete()


dirN = '../TriggerEff/METScale/optimum_with_phiSpikeFilter' 

bkgList = ['TTJets',  'WJets', 'ZJets','QCD']

# make plots comparing each data year to bkg year 

#varList = {
#	'MET':['MET [GeV]'],
#	'METPhi':['#phi(MET)'],
#	'AK8jet_phi_lead':['#phi(j_1)'],
#	'AK8jet_phi_sublead':['#phi(j_2)'],
#	'AK4jet_phi_lead':['#phi(j_1)'],
#	'AK4jet_phi_sublead':['#phi(j_2)']
#}

## Use these for TriggerEff files
varList = {
	'MET':['#slash{E}_{T} [GeV]'],
	'JetsAK8[0].Pt()':["Leading Jet p_{T} [GeV]"],
	'JetsAK8[1].Pt()':["Subleading Jet p_{T} [GeV]"],
	'JetsAK8[0].Eta()':["Leading Jet #eta"],
	'JetsAK8[1].Eta()':["Subleading Jet #eta"],
	'JetsAK8[0].Phi()':["Leading Jet #phi"],
	'JetsAK8[1].Phi()':["Subleading Jet #phi"],
	'JetsAK8_girth[0]':["girth(j_{1})"],
	'JetsAK8_girth[1]':["girth(j_{2})"],
	'JetsAK8_softDropMass[0]':["m_{SD}(j_{1}) [GeV]"],
	'JetsAK8_softDropMass[1]':["m_{SD}(j_{2}) [GeV]"],
	'JetsAK8_axismajor[0]':["#sigma_{major}(j_{1})"],
	'JetsAK8_axismajor[1]':["#sigma_{major}(j_{2})"],
	'JetsAK8_axisminor[0]':["#sigma_{minor}(j_{1})"],
	'JetsAK8_axisminor[1]':["#sigma_{minor}(j_{2})"],
	'JetsAK8_ptD[0]':["p_{T}D(j_{1})"],
	'JetsAK8_ptD[1]':["p_{T}D(j_{2})"],
	'JetsAK8_ecfN2b1[0]':["N_{2}^{(1)}(j_{1})"],
	'JetsAK8_ecfN2b1[1]':["N_{2}^{(1)}(j_{2})"],
	'JetsAK8_ecfN3b1[0]':["N_{3}^{(1)}(j_{1})"],
	'JetsAK8_ecfN3b1[1]':["N_{3}^{(1)}(j_{2})"],
	'JetsAK8_chargedHadronEnergyFraction[0]':["f_{h^{#pm}}(j_{1})"],
	'JetsAK8_chargedHadronEnergyFraction[1]':["f_{h^{#pm}}(j_{2})"],
	'JetsAK8_neutralHadronEnergyFraction[0]':["f_{h^{0}}(j_{1})"],
	'JetsAK8_neutralHadronEnergyFraction[1]':["f_{h^{0}}(j_{2})"],
	'JetsAK8_electronEnergyFraction[0]':["f_{e}(j_{1})"],
	'JetsAK8_electronEnergyFraction[1]':["f_{e}(j_{2})"],
	'JetsAK8_muonEnergyFraction[0]':["f_{#mu}(j_{1})"],
	'JetsAK8_muonEnergyFraction[1]':["f_{#mu}(j_{2})"],
	#'JetsAK8_photonEnergyFraction[0]':["f_{#gamma}(j_{1})"],
	#'JetsAK8_photonEnergyFraction[1]':["f_{#gamma}(j_{2})"],
	'metR':["#slash{E}_{T}/m_{T}"],
	'tau23_lead':['#tau_{32}(j_{1})'],
	'tau12_lead':['#tau_{21}(j_{1})'],
	'tau23_sub':['#tau_{32}(j_{2})'],
	'tau12_sub':['#tau_{21}(j_{2})'],
	'DeltaPhi1':["#Delta#phi(j_{1}, #slash{E}_{T})"],
	'DeltaPhi2':["#Delta#phi(j_{2}, #slash{E}_{T})"],
	'DeltaPhiMin_AK8':["#Delta#phi_{min}"],
	'DeltaEta':["#Delta#eta(j_{1},j_{2})"],
	'HT':["H_{T} (GeV)"],
	'MT_AK8':["m_{T} (GeV)"]
}
#varList = {
#	'MET':['MET [GeV]']
#}

# <var>_<sample>

bkgColorDict = {"QCD":602,"TTJets":798,"WJets":801,"ZJets":881} # Annapoala, Giorgia
#bkgColorDict = {"QCD":41,"TTJets":42,"WJets":43,"ZJets":44} # Colin

#for each year
	# for each filter
		# for each bkgground
		# for data
	# draw

#for year in ['16','17','18PRE','18POST']:
for year in ['16','17','18PRE','18POST']:
	for var in varList.keys():
		tB = rt.TH1F()
		tD = rt.TH1F()
		tQ = rt.TH1F()
		tT = rt.TH1F()
		tZ = rt.TH1F()
		tW = rt.TH1F()
		tS = rt.TH1F()
		tempHist = {"base":tB,"Data":tD,"QCD":tQ,"TTJets":tT,"WJets":tW,"ZJets":tZ}

		for bkgGroup in bkgList:
			bkgName = bkgGroup+year
			_file = rt.TFile.Open(dirN+"/"+bkgName+"/METScale.root","READ")
			_file.GetObject(var+"_"+bkgName,tempHist[bkgGroup])
			tempHist[bkgGroup] = tempHist[bkgGroup].Clone(tempHist[bkgGroup].GetName()+"_")
			tempHist[bkgGroup].SetDirectory(0)
			tempHist[bkgGroup].SetLineColor(rt.kBlack)
			tempHist[bkgGroup].SetLineWidth(1)
			tempHist[bkgGroup].SetFillColor(bkgColorDict[bkgGroup])
			tempHist[bkgGroup].SetFillStyle(1001)
			_file.Close()

		_file2 = rt.TFile.Open(dirN+"/"+"Data"+year+"/METScale.root","READ")
		_file2.GetObject(var+"_Data"+year,tempHist["Data"])
		tempHist["Data"] = tempHist["Data"].Clone(tempHist["Data"].GetName()+"_")
		tempHist["Data"].SetDirectory(0)
		_file2.Close()

		_file3 = rt.TFile.Open(dirN+"/"+"base"+"/METScale.root","READ")
		_file3.GetObject(var+"_base",tempHist["base"])
		tempHist["base"] = tempHist["base"].Clone(tempHist["base"].GetName()+"_")
		tempHist["base"].SetDirectory(0)
		tempHist["base"].SetLineColor(rt.kRed)
		tempHist["base"].SetLineStyle(4)
		_file3.Close()

		showLog = True


		makeRatioBkgStack(
			[tempHist["TTJets"],tempHist["WJets"],tempHist["ZJets"],tempHist["QCD"]], #bkg list
			tempHist["Data"], # data
			tempHist["base"], # signal
			varList[var][0]+" "+year, # title
			varList[var][0], # xlabel
			"Events", # ylabel
			dirN + '/pdf/' + var.translate(None,"_[]().")+"_"+year+"_ratio.pdf", #name
			doLeg = True, # doLegned
			log = showLog) # doLog
