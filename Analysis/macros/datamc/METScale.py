from analysisBase import baseClass
import ROOT as rt
import tdrstyle
from array import array

rt.gROOT.SetBatch(True)
rt.gStyle.SetOptTitle(1)
tdrstyle.setTDRStyle()

def loop(self):

	def GetCorr(var,fun):        # returns trigger efficiency; var = MTAK8, fun = fun16, fun17, or fun18
		if(var > fun.GetXmax()):
			var = fun.GetXmax()
		if(var < fun.GetXmin()):
			var = fun.GetXmin()
		return fun.Eval(var)

	# open Trigger Efficiency Formula files
	TE16 = rt.TFile.Open("macros/datamc/TriggerEfficiency/trigEffFit_SingleMuon_2016_DetaHLTmatch.root")
	fun16 = TE16.Get("fit_MTAK8")
	TE17 = rt.TFile.Open("macros/datamc/TriggerEfficiency/trigEffFit_SingleMuon_2017_DetaHLTmatch.root")
	fun17 = TE17.Get("fit_MTAK8")
	TE18 = rt.TFile.Open("macros/datamc/TriggerEfficiency/trigEffFit_SingleMuon_2018_DetaHLTmatch.root")
	fun18 = TE18.Get("fit_MTAK8")

	tree = self.getChain(self.treeNameList[0])

	# added friend tree
	nEvents = tree.GetEntries()
	print("n events = " + str(nEvents))


	# initalize histograms to be made, or create Friend tree to be filled
	self.outRootFile.cd()
	
	# maximum x value for each variable
	metx = 2000
	Phix = 3.3
# H_T
	# list of branches to plot
	plotDict = {#key = var name, value = [varType, nBins, binLow, binHigh, title]
				# varType can be "s" - single value (ie 'MET')
	'MET':["s",100,200,2000,self.fileID+";MET; Events"],
	'MHT':["s",100,200,2000,self.fileID+";MHT; Events"],
	'JetsAK8[0].Pt()':["vIF",100,0,3000,self.fileID+";Leading jet Pt;Events"],
	'JetsAK8[1].Pt()':["vIF",100,0,1800,self.fileID+";Subleading jet Pt;Events"],
	'JetsAK8[0].Eta()':["vIF",100,-2.5,2.5,self.fileID+";Jet Eta;Events"],
	'JetsAK8[1].Eta()':["vIF",100,-2.5,2.5,self.fileID+";Jet Eta;Events"],
	'JetsAK8[0].Phi()':["vIF",100,-3.2,3.2,self.fileID+";Jet Phi;Events"],
	'JetsAK8[1].Phi()':["vIF",100,-3.2,3.2,self.fileID+";Jet Phi;Events"],
	'JetsAK8_girth[0]':["vI",100,0,0.5,self.fileID+"; Girth; Events"],
	'JetsAK8_girth[1]':["vI",100,0,0.5,self.fileID+"; Girth; Events"],
	'JetsAK8_softDropMass[0]':["vI",100,0,600,self.fileID+"; SoftDrop Mass; Events"],
	'JetsAK8_softDropMass[1]':["vI",100,0,450,self.fileID+"; SoftDrop Mass; Events"],
	'JetsAK8_axismajor[0]':["vI",100,0,0.5,self.fileID+"; Major Axis; Events"],
	'JetsAK8_axismajor[1]':["vI",100,0,0.5,self.fileID+"; Major Axis; Events"],
	'JetsAK8_axisminor[0]':["vI",100,0,0.3,self.fileID+"; Minor Axis; Events"],
	'JetsAK8_axisminor[1]':["vI",100,0,0.3,self.fileID+"; Minor Axis; Events"],
	'JetsAK8_ptdrlog[0]':["vI",100,0,450,self.fileID+"; ptdrlog; Events"],
	'JetsAK8_ptdrlog[1]':["vI",100,0,450,self.fileID+"; ptdrlog; Events"],
	'JetsAK8_ptD[0]':["vI",100,0,1,self.fileID+"; ptD; Events"],
	'JetsAK8_ptD[1]':["vI",100,0,1,self.fileID+"; ptD; Events"],
	'JetsAK8_maxBvsAll[0]':["vI",100,0,1,self.fileID+"; maxBvsAll; Events"],
	'JetsAK8_maxBvsAll[1]':["vI",100,0,1,self.fileID+"; maxBvsAll; Events"],
	'JetsAK8_ecfN2b1[0]':["vI",100,0,0.5,self.fileID+"; ecfN2b1; Events"],
	'JetsAK8_ecfN2b1[1]':["vI",100,0,0.5,self.fileID+"; ecfN2b1; Events"],
	'JetsAK8_ecfN3b1[0]':["vI",100,0,4,self.fileID+"; ecfN3b1; Events"],
	'JetsAK8_ecfN3b1[1]':["vI",100,0,4,self.fileID+"; ecfN3b1; Events"],
	'JetsAK8_chargedHadronEnergyFraction[0]':["vI",100,0,1,self.fileID+"; fChgHad; Events"],
	'JetsAK8_chargedHadronEnergyFraction[1]':["vI",100,0,1,self.fileID+"; fChgHad; Events"],
	'JetsAK8_neutralHadronEnergyFraction[0]':["vI",100,0,1,self.fileID+"; fNeuHad; Events"],
	'JetsAK8_neutralHadronEnergyFraction[1]':["vI",100,0,1,self.fileID+"; fNeuHad; Events"],
	'JetsAK8_electronEnergyFraction[0]':["vI",100,0,1,self.fileID+"; fEle; Events"],
	'JetsAK8_electronEnergyFraction[1]':["vI",100,0,1,self.fileID+"; fEle; Events"],
	'JetsAK8_photonEnergyFraction[0]':["vI",100,0,1,self.fileID+"; fPhoton; Events"],
	'JetsAK8_photonEnergyFraction[1]':["vI",100,0,1,self.fileID+"; fPhoton; Events"],
	'JetsAK8_muonEnergyFraction[0]':["vI",100,0,1,self.fileID+"; fMu; Events"],
	'JetsAK8_muonEnergyFraction[1]':["vI",100,0,1,self.fileID+"; fMu; Events"],
	'detlaR12':["spec",100,0.8,3.5,self.fileID+";#Delta R(1,2);Events"],
	'metR':["spec",100,0.15,0.7,self.fileID+";MET/m_{T};Events"],
	'nJetsAK8':["spec",7,1,8,self.fileID+";nAK8 Jets;Events"],
	'nJetsAK4':["spec",40,0,40,self.fileID+";nAK4 Jets;Events"],
	'tau23_lead':["spec",100,0,7,self.fileID+";Leading Jet #tau_{23};Events"],
	'tau12_lead':["spec",100,0,15,self.fileID+";Subleading Jet #tau_{12};Events"],
	'tau23_sub':["spec",100,0,7,self.fileID+";Leading Jet #tau_{23};Events"],
	'tau12_sub':["spec",100,0,15,self.fileID+";Subeading Jet #tau_{12};Events"],
	'JetsAK8_bdtSVJtag[0]':["vI",100,0,1,self.fileID+"; SVJ BDT Output; Events"],
	'JetsAK8_bdtSVJtag[1]':["vI",100,0,1,self.fileID+"; SVJ BDT Output; Events"],
	'DeltaPhi1':["s",100,0,3.14,self.fileID+"; #Delta#phi(j_1, MET); Events"],
	'DeltaPhi2':["s",100,0,3.14,self.fileID+"; #Delta#phi(j_2, MET); Events"],
	'DeltaPhiMin_AK8':["s",100,0,Phix*1.01,self.fileID+";#Delta#phi_{min};Events"],
	'DeltaEta':["spec",100,0,1.6,self.fileID+";#Delta#eta(j_{1},j_{2});Events"],
	'NElectrons':["s",5,0,5,self.fileID+";Electrons multiplicity;Events"],
	'NMuons':["spec",5,0,5,self.fileID+";Muons multiplicity (miniIso<0.4);Events"],
	'HT':["s",100,0,5000,self.fileID+";#H_T (GeV);Events"],
	'JetsAK8_multiplicity[0]':["vI",100,0,200,self.fileID+";multiplicity for leading jet;Events"],
	'JetsAK8_multiplicity[1]':["vI",100,0,200,self.fileID+";multiplicity for subleading jet;Events"], # number of constituent particles in jet
	'MT_AK8':["s",100,1600,3800,self.fileID+";m_{T} (GeV);Events"]
	}
	branchList = tree.GetListOfBranches()
	branchListNames = []
	for thing in branchList:
		branchListNames.append(thing.GetName())
	tree.SetBranchStatus("*",0)
	tree.SetBranchStatus("RunNum" ,1)
	tree.SetBranchStatus("madHT",1)
	tree.SetBranchStatus("GenElectrons",1)
	tree.SetBranchStatus("GenMuons",1)
	tree.SetBranchStatus("GenTaus",1)
	tree.SetBranchStatus("GenMET",1)
	tree.SetBranchStatus("JetsAK8_NsubjettinessTau1",1)
	tree.SetBranchStatus("JetsAK8_NsubjettinessTau2",1)
	tree.SetBranchStatus("JetsAK8_NsubjettinessTau3",1)
	tree.SetBranchStatus("HEMOptVetoFilter" ,1)
	tree.SetBranchStatus("JetsAK8",1)
	tree.SetBranchStatus("Jets",1)
	tree.SetBranchStatus("MT_AK8",1)
	tree.SetBranchStatus("MET",1)
	tree.SetBranchStatus("METPhi",1)
	tree.SetBranchStatus("NVtx",1)	
	tree.SetBranchStatus("Muons_MiniIso",1)
	tree.SetBranchStatus("NElectrons",1)
	tree.SetBranchStatus("globalSuperTightHalo2016Filter",1)
	tree.SetBranchStatus("HBHENoiseFilter",1)
	tree.SetBranchStatus("HBHEIsoNoiseFilter",1)
	tree.SetBranchStatus("BadPFMuonFilter",1)
	tree.SetBranchStatus("BadChargedCandidateFilter",1)
	tree.SetBranchStatus("eeBadScFilter",1)
	tree.SetBranchStatus("PhiSpikeVetoFilter",1)
	tree.SetBranchStatus("TrueNumInteractions",1)
	for plotVar in plotDict.keys():
		if plotVar.split("[")[0] in branchListNames:
			tree.SetBranchStatus(plotVar.split("[")[0],1)
		else:
			print(plotVar.split("[")[0] +" not in tree")	

	if (("Jets" in self.fileID) or ("QCD" in self.fileID)): # only need to do this for MC bkg
		tree.SetBranchStatus("Weight",1)		# activate puWeight, puSysUp, puSysDown branches
		tree.SetBranchStatus("puWeightNew",1)

		if "16" in self.fileID:
			lumi = 35921.036
			print("2016 Lumi")
		elif "17" in self.fileID:
			lumi = 41521.331
			print("2017 Lumi")
		elif "18PRE" in self.fileID:
			lumi = 21071.460
			print("2018 pre Lumi")
		elif "18POST" in self.fileID:
			lumi = 38621.232
			print("2018 post Lumi")
		elif "18" in self.fileID:
			lumi = 59692.692
			print("2018 full lumi")
		else:
			print("Dont know what total lumi to use. default to 40 fb-1")
			lumi = 40000.
	else:
		lumi = 1
	histDict = {}

	for plotVar, histSpecs in plotDict.items():
		if len(histSpecs) > 6:
			histDict[plotVar] = self.makeTH2F(plotVar+"_"+self.fileID,histSpecs[7],histSpecs[1],histSpecs[2],histSpecs[3],histSpecs[4],histSpecs[5],histSpecs[6]) # 2D plots
		else:
			histDict[plotVar] = self.makeTH1F(plotVar+"_"+self.fileID,histSpecs[4],histSpecs[1],histSpecs[2],histSpecs[3]) # 1D plots
	
	WtotE = 0
	totE = 0
	CtotE = 0
	vcount = 0
	
	for iEvent in range(nEvents):
		if iEvent%1000 == 0:
			print("Event: " + str(iEvent) + "/" + str(nEvents))
		tree.GetEvent(iEvent)		
		
		if (("Jets" in self.fileID) or ("QCD" in self.fileID)): # or ("ST1" in self.fileID)): # Bkg MC get tree weight, data and signal MC get weight == 1		
			weight = (tree.Weight)*(tree.puWeightNew)
		else: 
			weight = 1.

# 		Applying constant scaling to QCD
		if "QCD" in self.fileID:
			if "16" in self.fileID:
				weight = weight * 1.0  # 1.2
			elif "17" in self.fileID:
				weight = weight * 1.0  # 2.0
			elif "18PRE" in self.fileID:
				weight = weight * 1.0  # 1.5
			elif "18POST" in self.fileID:
				weight = weight * 1.0  # 1.5

#		HEM Veto
		if "18" in self.fileID:
			if (("PRE" in self.fileID) and ("Data" in self.fileID) and (tree.RunNum >= 319077)):
				continue
			elif "POST" in self.fileID:
				if ( ( ("Data" in self.fileID) and (tree.RunNum < 319077) ) or (tree.HEMOptVetoFilter == 0) ):
					continue

# 		important variables
		FJets = tree.JetsAK8
		Jets = tree.Jets
		MET = tree.MET
		METPhi = tree.METPhi
		MTAK8 = tree.MT_AK8

		# MET filters
		gSTH = tree.globalSuperTightHalo2016Filter
		HBHEN = tree.HBHENoiseFilter
		HBHEIN = tree.HBHEIsoNoiseFilter
		BPFM = tree.BadPFMuonFilter
		BCC = tree.BadChargedCandidateFilter
		eeBS = tree.eeBadScFilter
		nV = tree.NVtx
		EDCTP = tree.EcalDeadCellTriggerPrimitiveFilter

		# Calculating trigger efficiency
		tEff = 0

		if (("Jets" in self.fileID) or ("QCD" in self.fileID)): # apply for Background MC only
			if "16" in self.fileID:			
				tEff = GetCorr(MTAK8,fun16)
			if "17" in self.fileID:			
				tEff = GetCorr(MTAK8,fun17)
			if "18" in self.fileID:			
				tEff = GetCorr(MTAK8,fun18)
		else:
			tEff = 1.

# MET Filters (all except for EcalDeadCellTriggerPrimitiveFilter
		if not(gSTH == 1 and HBHEN == 1 and HBHEIN == 1 and BCC == 1 and eeBS == 1 and BPFM==1 and nV > 0):
			continue

		
# 		phi spike filters
		if tree.PhiSpikeVetoFilter != 1:
			continue

#		Keeping track of the number of events
		WtotE += weight*lumi
		totE += 1
		CWeight = weight*lumi*tEff
		CtotE += CWeight

# 		Filling histograms	
		for plotVar in plotDict.keys():
			if plotDict[plotVar][0] == "s": # branch
				#print(plotVar)
				histDict[plotVar].Fill(getattr(tree,plotVar),CWeight)
			elif plotDict[plotVar][0] == "sF": # branch.func()
				varStrHelper = plotVar.split(".")
				bName, bFunc = varStrHelper[0],varStrHelper[1][:-2]
				#print(bname, bFunc)
				histDict[plotVar].Fill(getattr(getattr(tree, bName), bFunc)(), CWeight)
			elif plotDict[plotVar][0] == "vA": # branch
				#print(plotVar)
				for value in getattr(tree,plotVar):
					histDict[plotVar].Fill(value,CWeight)
			elif plotDict[plotVar][0] == "vI": # branch[index]
				varStrHelper = plotVar.replace("]","[").split("[")
				bName, bIndex = varStrHelper[0],varStrHelper[1]
				#print(bName, bIndex)
				histDict[plotVar].Fill(getattr(tree,bName)[int(bIndex)],CWeight)
			elif plotDict[plotVar][0] == "vAF":# branch.func()
				bName, bFunc = plotVar.split(".")[0],plotVar.split(".")[1][:-2]
				#print(bName, bFunc)
				for value in getattr(tree,bName):
					histDict[plotVar].Fill(getattr(value, bFunc)(),CWeight)
			elif plotDict[plotVar][0] == "vIF":# branch[index].func()
				varStrHelper = plotVar.replace("]","[").replace("[",".").split(".")
				bName, bIndex, bFunc = varStrHelper[0],varStrHelper[1],varStrHelper[3][0:-2]
				histDict[plotVar].Fill(getattr(getattr(tree,bName)[int(bIndex)],bFunc)(),CWeight)

		#special ones that don't fit the normal stuff
		detlaR12 = tree.JetsAK8[0].DeltaR(tree.JetsAK8[1])
		deltaEta = abs(FJets[0].Eta()- FJets[1].Eta())
		metR = tree.MET/tree.MT_AK8
		nJetsAK8 = len(tree.JetsAK8)
		nJetsAK4 = len(tree.Jets)

		mmIso = tree.Muons_MiniIso
		nMuon = 0

		if (mmIso.size() > 0):
			for imm in range(mmIso.size()):
				if mmIso[imm] < 0.4:
					nMuon += 1

		try:
			tau23_lead = tree.JetsAK8_NsubjettinessTau2[0]/tree.JetsAK8_NsubjettinessTau3[0]
		except ZeroDivisionError:
			tau23_lead = 0
		try:
			tau12_lead = tree.JetsAK8_NsubjettinessTau1[0]/tree.JetsAK8_NsubjettinessTau2[0]
		except ZeroDivisionError:
			tau12_lead = 0
		try:
			tau23_sub = tree.JetsAK8_NsubjettinessTau2[1]/tree.JetsAK8_NsubjettinessTau3[1]
		except ZeroDivisionError:
			tau23_sub = 0
		try:
			tau12_sub = tree.JetsAK8_NsubjettinessTau1[1]/tree.JetsAK8_NsubjettinessTau2[1]
		except ZeroDivisionError:
			tau12_sub = 0

		histDict['detlaR12'].Fill(detlaR12,CWeight)
		histDict['metR'].Fill(metR,CWeight)
		histDict['nJetsAK8'].Fill(nJetsAK8,CWeight)
		histDict['nJetsAK4'].Fill(nJetsAK4,CWeight)
		histDict['tau23_lead'].Fill(tau23_lead,CWeight)
		histDict['tau12_lead'].Fill(tau12_lead,CWeight)
		histDict['tau23_sub'].Fill(tau23_sub,CWeight)
		histDict['tau12_sub'].Fill(tau12_sub,CWeight)

		histDict['DeltaEta'].Fill(deltaEta,CWeight)
		histDict['NMuons'].Fill(nMuon,CWeight)


	print("Number of events:")
	print totE			
	print("Weighted number of events:")
	print WtotE
	print("Weighted number of events with trigger efficiency:")
	print CtotE

def addLoop():
	baseClass.loop = loop

