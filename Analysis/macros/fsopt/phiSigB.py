from analysisBase import baseClass
import ROOT as rt
import tdrstyle
from array import array
import numpy as np

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

	def MinDist(etaList,phiList,ijet):
		distList = []

		for iv in range(len(etaList)):
			etaV = etaList[iv]
			phiV = phiList[iv]

			distV = (ijet.Eta() - etaV)**2 + (ijet.Phi() - phiV)**2			
			distList.append(distV)
		return np.amin(distList)

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

	# creating tree and branches to save the results
	rtree = self.makeTree('rtree','tree with minimum distances')

	d16 = array( 'f', [ 0 ] )
	d17 = array( 'f', [ 0 ] )
	d18PRE = array( 'f', [ 0 ] )
	d18POST = array( 'f', [ 0 ] ) 
	CW = array( 'f', [ 0 ] ) 

	rtree.Branch( 'Dist_to_HS_16', d16, 'Dist_to_HS_16/F' )
	rtree.Branch( 'Dist_to_HS_17', d17, 'Dist_to_HS_17/F' )
	rtree.Branch( 'Dist_to_HS_18PRE', d18PRE, 'Dist_to_HS_18PRE/F' )
	rtree.Branch( 'Dist_to_HS_18POST', d18POST, 'Dist_to_HS_18POST/F' )
	rtree.Branch( 'Event_Weight', CW, 'Event_Weight/F' )

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
	tree.SetBranchStatus("EcalDeadCellTriggerPrimitiveFilter",1)

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
	
	WtotE = 0
	totE = 0
	CtotE = 0
	
	for iEvent in range(nEvents):
		if iEvent%1000 == 0:
			print("Event: " + str(iEvent) + "/" + str(nEvents))
		tree.GetEvent(iEvent)

		if "TT" in self.fileID:
			if self.stitchTT(tree.GetFile().GetName().split("/")[-1], tree.madHT, len(tree.GenElectrons),len(tree.GenMuons), len(tree.GenTaus), tree.GenMET, self.fileID):
				continue		
		
		if (("Jets" in self.fileID) or ("QCD" in self.fileID)): # or ("ST1" in self.fileID)): # Bkg MC get tree weight, data and signal MC get weight == 1		
			weight = (tree.Weight)*(tree.puWeightNew)
		else: 
			weight = 1.
		
		if "18" in self.fileID:
			if (("PRE" in self.fileID) and ("Data" in self.fileID) and (tree.RunNum >= 319077)):
				continue
			elif "POST" in self.fileID:
				if ( ( ("Data" in self.fileID) and (tree.RunNum < 319077) ) or (tree.HEMOptVetoFilter == 0) ):
					continue

		# important variables
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
			tEff = 1

		CWeight = weight*lumi*tEff

		# MET Filters (all except for EcalDeadCellTriggerPrimitiveFilter
		if not(gSTH == 1 and HBHEN == 1 and HBHEIN == 1 and BCC == 1 and eeBS == 1 and BPFM==1 and nV > 0):
			continue

		lowMTlim = 2000.0
		highMTlim = 4000.0

		if lowMTlim > tree.MT_AK8 or tree.MT_AK8 > highMTlim:
			continue

		# lists of eta and phi values of hot spots
		etaList16 = [-1.2,-0.912,-0.912,-0.816,-0.72,-0.72,-0.528,-0.432,-0.336,-0.24,
-0.24,-0.144,-0.144,-0.048,0.144,0.912,0.912,1.008,1.296,-1.584,-0.816,-0.72,-0.144,-0.048,-0.048,0.048,1.104,1.488]
		phiList16 =[-1.19,2.03,3.01,-1.75,-2.17,-0.77,2.73,2.73,0.21,0.07,0.21,-2.59,
0.77,0.91,1.75,1.75,2.87,0.63,-0.49,0.63,1.47,-2.31,0.07,-2.59,0.77,0.91,-3.15,2.73]
		etaList17 = [-0.912,-0.912,-0.816,-0.72,-0.528,-0.336,-0.24,-0.24,-0.144,-0.144,
-0.048,0.144,0.912,0.912,1.008,-1.2,-0.72,-0.72,-0.432,0.336,0.624,1.104,1.296]
		phiList17 = [2.03,3.01,-1.75,-0.77,2.73,0.21,0.07,0.21,-2.59,0.77,0.91,1.75,1.75,
2.87,0.63,-1.19,-2.31,-2.17,2.73,-0.77,-0.77,-3.15,-0.49]
		etaList18PRE = [-1.584,-1.2,-0.912,-0.912,-0.816,-0.816,-0.72,-0.72,-0.528,-0.432,
-0.336,-0.24,-0.24,-0.144,-0.144,-0.144,-0.048,-0.048,0.144,0.912,0.912,1.008,1.296,-0.72,1.104,1.488,1.776]
		phiList18PRE = [0.63,-1.19,2.03,3.01,-1.75,-0.77,-2.17,-0.77,2.73,2.73,0.21,0.07,
0.21,-2.59,0.07,0.77,0.77,0.91,1.75,1.75,2.87,0.63,-0.49,-2.31,-3.15,-0.21,0.77]
		etaList18POST = [-1.2,-0.912,-0.912,-0.816,-0.72,-0.528,-0.336,-0.24,-0.24,-0.144,
-0.144,-0.048,0.144,0.912,0.912,1.008,1.296,-1.584,-0.816,-0.72,-0.72,-0.432,-0.144,-0.048,1.104,1.488,1.776]
		phiList18POST = [-1.19,2.03,3.01,-1.75,-0.77,2.73,0.21,0.07,0.21,-2.59,0.77,0.91,
1.75,1.75,2.87,0.63,-0.49,0.63,-0.77,-2.31,-2.17,2.73,0.07,0.77,-3.15,-0.21,0.77]

		d16[0] = MinDist(etaList16,phiList16,Jets[1])
		d17[0] = MinDist(etaList17,phiList17,Jets[1])
		d18PRE[0] = MinDist(etaList18PRE,phiList18PRE,Jets[1])
		d18POST[0] = MinDist(etaList18POST,phiList18POST,Jets[1])
		CW[0] = CWeight
		
		rtree.Fill()

def addLoop():
	baseClass.loop = loop

