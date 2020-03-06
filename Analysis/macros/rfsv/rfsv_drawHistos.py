import ROOT as rt
import sys
import CMS_lumi, tdrstyle

tdrstyle.setTDRStyle()

#rt.gStyle.SetPalette(54,0)
rt.gROOT.SetBatch(True)
rt.gStyle.SetOptStat(0)

#listOfDudes = [
#["3000","20","0.3","peak", .184, .141],
#["2000","20","0.3","peak",.168,.163],
#["4000","20","0.3","peak",.147,.163],
#["3000","50","0.3","peak",.135,.105],
#["3000","100","0.3","peak",.141,.141],
#["3000","20","0.5","peak",.189,.180],
#["3000","20","0.7","peak",.201,.174],
#["3000","20","0.3","low",.163,.138],
#["3000","20","0.3","high",.160,.126]]

listOfDudes = [
["3000","20","0.3","peak", .184, .141]]


#print("dSet mZ mD rI a nB nD fD rD iH fH rH")
print("iBin MT Base Double Half")
saveDir = "plots_ANbins_3/"
for mZprime, mDark, rInv, Alpha, errorR, errorF in listOfDudes:
	idString = "mZprime-{}_mDark-{}_rinv-{}_alpha-{}".format(mZprime, mDark, rInv, Alpha)

	histMax = 4000		# Keane
	if mZprime == "2000":	# Keane
		histMax = 2500	# Keane
	elif mZprime == "4000":	# Keane
		histMax = 4500	# Keane

	histLimsDict = {
	"eventMT":[24, 1500, histMax],	# Keane
	"jet0Pt":[30, 0, 3000],
	"jet1Pt":[30, 0, 3000],
	"jet0Eta":[11, -2.4, 2.4],
	"jet1Eta":[11, -2.4, 2.4],
	'eventRT':[25, 0.0, 1.0],
	'eventMET':[32, 100, 1600]}
	
	#take rf, xH and xD
	# plot the suckers ontop of one another.
	# color xH red for half
	# color xD green for Double
	# color rf black for base
	for dSet in ["r","f"]:
		if dSet == "r":
			DSET = "Renormlization"
			error = errorR
		elif dSet == "f":
			DSET = "Factorization"
			error = errorF
		_fileBase = rt.TFile.Open("Skims/rf_"+idString+".root","read")
		_fileHalf = rt.TFile.Open("Skims/"+dSet+"H_"+idString+".root","read")
		_fileDoub = rt.TFile.Open("Skims/"+dSet+"D_"+idString+".root","read")

		treeBase = _fileBase.Get("tree_rf")
		treeHalf = _fileHalf.Get("tree_"+dSet+"H")
		treeDoub = _fileDoub.Get("tree_"+dSet+"D")

		selcJetPt = "(jet0Pt>200)&&(jet1Pt>200)"
		selcJetEta = "(abs(jet0Eta)<2.4)&&(abs(jet1Eta)<2.4)"
		selcJetAbsEta = "(abs(jet0Eta-jet1Eta)<1.5)"
		selcRTMT = "(eventRT>0.15)&&(eventMT>1500)"
		preSelc = selcJetPt+"&&"+selcJetEta+"&&"+selcJetAbsEta+"&&"+selcRTMT
		#preSelc = ""
		for var in ["eventMT"]:#, "jet0Pt", "jet1Pt", "jet0Eta","jet1Eta",'eventRT','eventMET']:

			H=700
			W=700

			H_ref = 700
			W_ref = 700

			T = 0.08*H_ref
			B = 0.12*H_ref
			L = 0.12*W_ref
			R = 0.08*W_ref

			c = rt.TCanvas("c","canvas",0,0,W,H)
			c.SetFillColor(0);
			c.SetBorderMode(0);
			c.SetFrameFillStyle(0);
			c.SetFrameBorderMode(0);
			#c.SetLeftMargin( 0.15 );#L/W                       
			c.SetRightMargin(0.04);                                                                                                              
			#c.SetRightMargin( R/W );
			c.SetTopMargin( T/H );
			#c.SetBottomMargin(0.2);
			c.SetTickx(0);
			c.SetTicky(0);
			c.Draw()
			c.SetLogy()

			hist_Base = rt.TH1F("hB",DSET+" "+idString.replace("-","=").replace("_",", ")+";"+var+";Events",histLimsDict[var][0],histLimsDict[var][1],histLimsDict[var][2])
			hist_Half = rt.TH1F("hH",DSET+" "+idString.replace("-","=").replace("_",", ")+";"+var+";Events",histLimsDict[var][0],histLimsDict[var][1],histLimsDict[var][2])
			hist_Doub = rt.TH1F("hD",DSET+" "+idString.replace("-","=").replace("_",", ")+";"+var+";Events",histLimsDict[var][0],histLimsDict[var][1],histLimsDict[var][2])
			hist_Base.Sumw2()
			hist_Half.Sumw2()
			hist_Doub.Sumw2()

			pad1 = rt.TPad("pad1", "pad1", 0, 0.25, 1, 0.95)
			pad1.SetBottomMargin(0.05)
			pad1.SetRightMargin(0.04)
			#pad1.SetGridx()         # Vertical grid
			#pad1.SetGridy()         # Horizontal grid
			pad1.SetLogy()
			pad1.Draw()             # Draw the upper pad: pad1
			pad1.cd()               # pad1 becomes the current pad

			treeBase.Draw(var+">>hB",preSelc,"hist SAME")
			treeHalf.Draw(var+">>hH",preSelc,"hist SAME")
			treeDoub.Draw(var+">>hD",preSelc,"hist SAME")
#			hist_BaseError = hist_Base.Clone("hBE")
#			for iBin in range(1, hist_BaseError.GetNbinsX()+1):
#				hist_BaseError.SetBinError(iBin, hist_BaseError.GetBinContent(iBin)*error)
			#hist_Base = rt.gDirectory.Get("hB")
			#hist_Half = rt.gDirectory.Get("hH")
			#hist_Doub = rt.gDirectory.Get("hD")
			hist_Base.SetLineColor(rt.kBlack)
			hist_Half.SetLineColor(rt.kRed)
			hist_Doub.SetLineColor(rt.kBlue)

			hist_Base.GetXaxis().SetLabelOffset(999)
			hist_Base.GetXaxis().SetLabelSize(0)
			hist_Base.GetYaxis().SetTitle("Events")
			hist_Base.GetYaxis().SetTitleSize(30)
			hist_Base.GetYaxis().SetTitleFont(43)
			hist_Base.GetYaxis().SetTitleOffset(1.35)
			hist_Base.GetYaxis().SetLabelFont(43)
			hist_Base.GetYaxis().SetLabelSize(25)
			hist_Base.SetMaximum(6000)

			if DSET == "Renormlization":
				dname = "Renorm."
			elif DSET == "Factorization":
				dname = "Fact."

			leg = rt.TLegend(0.65,0.7,0.85,0.9)
			leg.SetTextFont(42)
			leg.SetHeader("SVJ_3000_20_0.3_peak")
			leg.AddEntry(hist_Base, dname+" central","l")
			leg.AddEntry(hist_Doub, dname+" Double","l")
			leg.AddEntry(hist_Half, dname+" Half","l")
			leg.SetTextSize(.04)
			leg.Draw("same")
			#hist_BaseError.SetFillColorAlpha(rt.kBlack,0.5)
			#hist_BaseError.Draw("same e2")
			hist_Half.SetLineStyle(7)
			hist_Doub.SetLineStyle(7)
			hist_Half.SetLineWidth(2)
			hist_Doub.SetLineWidth(2)
			hist_Base.SetTitle(DSET+" "+idString.replace("-","=").replace("_",", ")+";"+var+";Events")
			hist_Half.SetTitle(DSET+" "+idString.replace("-","=").replace("_",", ")+";"+var+";Ratio")
			hist_Doub.SetTitle(DSET+" "+idString.replace("-","=").replace("_",", ")+";"+var+";Ratio")
			c.Update()

#			for iBin in range(1, hist_Doub.GetNbinsX()+1):
#				print("{} {} {} {} {} {} {} {} {} {} {}".format(dSet, mZprime, mDark, rInv, Alpha, iBin, hist_Base.GetBinLowEdge(iBin), hist_Base.GetBinContent(iBin),hist_Doub.GetBinContent(iBin), hist_Half.GetBinContent(iBin), error))
			# lower plot will be in pad2
			c.cd()          # Go back to the main canvas before defining pad2
			pad2 = rt.TPad("pad2", "pad2", 0, 0, 1, 0.25)
			pad2.SetTopMargin(0.05)
			pad2.SetBottomMargin(0.37)
			pad2.SetRightMargin(0.04)
			#pad2.SetGridx() # vertical grid
			#pad2.SetGridy()         # Horizontal grid
			pad2.Draw()
			pad2.cd()       # pad2 becomes the current pad

			iH = hist_Half.Integral()
			iB = hist_Base.Integral()
			iD = hist_Doub.Integral()
			c.SetLogy(0)
			h3 = hist_Doub.Clone("h3")
			h3.Divide(hist_Base)
			h3.SetMinimum(0.78) # Keane
			h3.SetMaximum(1.22) # Keane
			h3.GetXaxis().SetTitleSize(33)
			h3.GetXaxis().SetTitleFont(43)
			h3.GetYaxis().SetTitle("syst/central")
			h3.GetYaxis().SetTitleSize(30)
			h3.GetYaxis().SetTitleFont(43)
			h3.GetYaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
			h3.GetYaxis().SetLabelSize(22)
			h3.GetYaxis().SetNdivisions(503)
			h3.SetMarkerStyle(8)
			h3.SetMarkerColor(rt.kBlue)
			h3.GetXaxis().SetTitle("M_{T} [GeV]")
			h3.GetXaxis().SetTitleSize(33)
			h3.GetXaxis().SetTitleFont(43)
			h3.GetXaxis().SetTitleOffset(3.2)
			h3.GetXaxis().SetLabelFont(43) # Absolute font size in pixel (precision 3)
			h3.GetXaxis().SetLabelSize(22)
			h3.GetXaxis().SetLabelOffset(0.03)

			h4 = hist_Half.Clone("h4")
			h4.Divide(hist_Base)
			h4.SetMarkerStyle(8)
			h4.SetMarkerColor(rt.kRed)
			lineDoub = rt.TF1("lD","[0]")
			lineHalf = rt.TF1("lH","[0]")
			error = 0.15 # Keane
			line_Low = rt.TF1("lLow",str(1-error),1500,4500)
			line_Hi = rt.TF1("lHi",str(1+error),1500,4500)
			line_Low.SetLineColor(rt.kBlack)
			line_Hi.SetLineColor(rt.kBlack)
			h3.Fit(lineDoub,"LQCN")
			h4.Fit(lineHalf,"LCQN")
			fD = lineDoub.GetParameter(0)
			fH = lineHalf.GetParameter(0)
			h3.Draw("EX0P")
			h4.Draw("EX0P same")
			#line_Low.Draw("same")
			#line_Hi.Draw("same")

			const = rt.TF1("const", '[0]', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
			line = rt.TF1("line", '[0]+[1]*x', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
			one = rt.TF1("one", '1', h3.GetXaxis().GetXmin(), h3.GetXaxis().GetXmax())
			one.SetLineStyle(2)
			#h3.Fit("const","Q")
			one.SetLineColor(rt.kRed)
			one.Draw("same")

			# CMS style
			CMS_lumi.lumi_sqrtS = "41.5 fb^{-1} (13 TeV)"
			CMS_lumi.extraText   = "  Simulation"

			iPeriod = 0
			iPos = 0

			CMS_lumi.CMS_lumi(c, iPeriod, iPos)
			c.cd()
			c.Update();
			c.RedrawAxis()

			c.SaveAs(saveDir+var+"_"+DSET+"_"+idString.replace(".","p")+".pdf")
			#print("{} {} {} {} {} {} {} {} {} {} {} {}".format(dSet, mZprime, mDark, rInv, Alpha, iB, iD, fD, float(iB)/iD, iH, fH, float(iB)/iH))
