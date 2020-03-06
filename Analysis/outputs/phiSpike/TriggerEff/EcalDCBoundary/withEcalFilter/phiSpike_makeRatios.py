import ROOT as rt
rt.gROOT.SetBatch(True)

def makeRatioBkgStack(bkgList, data , title, xlabel, ylabel, name, doLeg = True, log = False):
	# bkgList is list of bkgHistos
	# data should be a TH1 of data
	# title is the histogram title
	# xlabel is histogram's x axis title
	# ylabel is histogram's y axis title
	# name is what the .png file will be named.

	# C++ Author: Olivier Couet, adapted to python by Colin Fallon
	# Define the Canvas
	c = rt.TCanvas("c", "canvas", 800, 800)
	# define stack of bkgHistos
	stack = rt.THStack()
	for histo in bkgList:
		stack.Add(histo)
	# Upper plot will be in pad1
	pad1 = rt.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
	pad1.SetBottomMargin(0) # Upper and lower plot are joined
	pad1.SetGridx()         # Vertical grid
	pad1.SetGridy()         # Horizontal grid
	if log:
		pad1.SetLogy()
	pad1.Draw()             # Draw the upper pad: pad1
	pad1.cd()               # pad1 becomes the current pad
	#stack.SetStats(0)       # No statistics on upper plot
	#data.SetStats(0)       # No statistics on upper plot
	stack.SetMinimum(1)
	stack.SetMaximum(40000)
	stack.Draw("hist")  
	data.Draw("E1 same")
	stack.GetYaxis().SetTitle(ylabel)
	if doLeg:
		if (("deltaR" in xlabel) or ("Eta" in xlabel) or ("ptD" in xlabel) or ("BvsAll" in xlabel) or ("ecf" in xlabel) or ("chgH" in xlabel)):
			leg = rt.TLegend(0.3,0.0,0.7,0.3,title,"brNDC") # pos bot mid
		else:		
			leg = rt.TLegend(0.5,0.6,0.9,0.9,title,"brNDC") # pos top right
		leg.SetNColumns(2)
		leg.AddEntry(data,"Data","EP")
		leg.AddEntry(0,"","")
		for hist in bkgList[::-1]:
			histID = hist.GetName()
			if "QCD" in histID:
				histID = "QCD"
			if "TTJets" in histID:
				histID = "TTJets"
			if "WJets" in histID:
				histID = "WJets"
			if "ZJets" in histID:
				histID = "ZJets"
			leg.AddEntry(hist, histID, "F" )
		ks = stack.GetStack().Last().KolmogorovTest(data)
		chi2 = stack.GetStack().Last().Chi2Test(data,"CHI2/NDF")
		leg.AddEntry(0,"KS = {:.2f}, #chi^2/ndf = {:.2f}".format(ks, chi2),"")
		leg.Draw()
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
	pad2 = rt.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
	pad2.SetTopMargin(0)
	pad2.SetBottomMargin(0.2)
	pad2.SetGridx() # vertical grid
	pad2.SetGridy()         # Horizontal grid
	pad2.Draw()
	pad2.cd()       # pad2 becomes the current pad

	# Define the ratio plot
	totBkg = stack.GetStack().Last()
	h3 = data.Clone("h3")
	h3.SetLineColor(rt.kBlack)
	h3.SetMinimum(0.50)  # Define Y ..
	h3.SetMaximum(1.50) # .. range
	h3.Sumw2()
	h3.SetStats(0)      # No statistics on lower plot
	h3.Divide(totBkg)
	h3.SetMarkerStyle(21)
	h3.Draw("ep")       # Draw the ratio plot

	# data settings
	data.SetMarkerColor(rt.kBlack)

	# Y axis h1 plot settings
	data.GetYaxis().SetTitleSize(20)
	data.GetYaxis().SetTitleFont(43)
	data.GetYaxis().SetTitleOffset(1.55)

	# Ratio plot (h3) settings
	h3.SetTitle("") # Remove the ratio title

	# Y axis ratio plot settings
	h3.GetYaxis().SetTitle("Data/Bkg")
	h3.GetYaxis().SetNdivisions(505)
	h3.GetYaxis().SetTitleSize(20)
	h3.GetYaxis().SetTitleFont(43)
	h3.GetYaxis().SetTitleOffset(1.55)
	h3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
	h3.GetYaxis().SetLabelSize(15)

	# X axis ratio plot settings
	h3.GetXaxis().SetTitle(xlabel)
	h3.GetXaxis().SetTitleSize(20)
	h3.GetXaxis().SetTitleFont(43)
	h3.GetXaxis().SetTitleOffset(4.)
	h3.GetXaxis().SetLabelFont(43); # Absolute font size in pixel (precision 3)
	h3.GetXaxis().SetLabelSize(15)

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
	#h3.Fit("line","Q+")
	#save as .png
	c.SaveAs(name)
	c.Delete()

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
	'MET':['MET [GeV]'],
	'METPhi':['#phi(MET)'],
	'AK8jet[0]_phi':['#phi(j_1)'],
	'AK8jet[1]_phi':['#phi(j_2)'],
	'AK4jet[0]_phi':['#phi(j_1)'],
	'AK4jet[1]_phi':['#phi(j_2)']
}

# <var>_<sample>

bkgColorDict = {"QCD":602,"TTJets":798,"WJets":801,"ZJets":881}

#for each year
	# for each filter
		# for each bkgground
		# for data
	# draw

for year in ['16']:
	for var in varList.keys():
		tD = rt.TH1F()
		tQ = rt.TH1F()
		tT = rt.TH1F()
		tZ = rt.TH1F()
		tW = rt.TH1F()
		tS = rt.TH1F()
		tempHist = {"Data":tD,"QCD":tQ,"TTJets":tT,"WJets":tW,"ZJets":tZ}

		for bkgGroup in bkgList:
			bkgName = bkgGroup+year
			_file = rt.TFile.Open(bkgName+"/EcalDCBoundaryFilter.root","READ")
			_file.GetObject(var+"_"+bkgName,tempHist[bkgGroup])
			tempHist[bkgGroup] = tempHist[bkgGroup].Clone(tempHist[bkgGroup].GetName()+"_")
			tempHist[bkgGroup].SetDirectory(0)
			tempHist[bkgGroup].SetLineColor(bkgColorDict[bkgGroup])
			tempHist[bkgGroup].SetFillColor(bkgColorDict[bkgGroup])
			tempHist[bkgGroup].SetFillStyle(1001)
			_file.Close()
		_file2 = rt.TFile.Open("Data"+year+"/EcalDCBoundaryFilter.root","READ")
		_file2.GetObject(var+"_Data"+year,tempHist["Data"])
		tempHist["Data"] = tempHist["Data"].Clone(tempHist["Data"].GetName()+"_")
		tempHist["Data"].SetDirectory(0)
		_file2.Close()

		showLog = True


		makeRatioBkgStack(
			[tempHist["TTJets"],tempHist["WJets"],tempHist["ZJets"],tempHist["QCD"]], #bkg list
			tempHist["Data"], # data
			varList[var][0]+" "+year, # title
			varList[var][0], # xlabel
			"Events", # ylabel
			var.translate(None,"_[]().")+"_"+year+"_ratio.png", #name
			doLeg = True, # doLegned
			log = showLog) # doLog
