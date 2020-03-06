from analysisBase import baseClass
import ROOT as rt
import tdrstyle
from array import array

rt.gROOT.SetBatch(True)
rt.gStyle.SetOptTitle(1)
tdrstyle.setTDRStyle()

def loop(self):
	# set up trees or chains
	#f = rt.TFile.Open(self.inputFileList[0])
	#tree = f.Get(self.treeNameList[0])	

	tree = self.getChain(self.treeNameList[0])

	# added friend tree
	nEvents = tree.GetEntries()
	print("n events = " + str(nEvents))


	# initalize histograms to be made, or create Friend tree to be filled
	self.outRootFile.cd()
	
	# maximum x value for each variable
	metx = 2000
	metPhix = 3.3

	# list of branches to plot
	plotDict = {#key = var name, value = [varType, nBins, binLow, binHigh, title]
				# varType can be "s" - single value (ie 'MET')
	'AK8jet_etaphi_lead':["s",50,-2.4,2.4,50,-3.5,3.5,self.fileID+";AK8jet_etaphi_lead; Events"],
	'AK8jet_etaphi_sublead':["s",50,-2.4,2.4,50,-3.5,3.5,self.fileID+";AK8jet_etaphi_sublead; Events"],
	'AK4jet_etaphi_lead':["s",50,-2.4,2.4,50,-3.5,3.5,self.fileID+";AK4jet_etaphi_lead; Events"],
	'AK4jet_etaphi_sublead':["s",50,-2.4,2.4,50,-3.5,3.5,self.fileID+";AK4jet_etaphi_sublead; Events"],
	'MET':["s",100,200,metx*1.01,self.fileID+";MET; Events"],
	'METPhi':["s",100,0,metPhix*1.01,self.fileID+";#phi(MET); Events"],
	'AK8jet_phi_lead':["s",100,0,metPhix*1.01,self.fileID+";#phi(j_1); Events"],
	'AK8jet_phi_sublead':["s",100,0,metPhix*1.01,self.fileID+";#phi(j_2); Events"],
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
	tree.SetBranchStatus("HEMOptVetoFilter" ,1)
	tree.SetBranchStatus("JetsAK8",1)
	tree.SetBranchStatus("Jets",1)
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

	print self.fileID

	totE = 0
		
	for iEvent in range(nEvents):
		if iEvent%1000 == 0:
			print("Event: " + str(iEvent) + "/" + str(nEvents))
		tree.GetEvent(iEvent)

		# important variables
		FJets = tree.JetsAK8
		Jets = tree.Jets
		MET = tree.MET
		METPhi = tree.METPhi
		# MET filters
		gSTH = tree.globalSuperTightHalo2016Filter
		HBHEN = tree.HBHENoiseFilter
		HBHEIN = tree.HBHEIsoNoiseFilter
		BPFM = tree.BadPFMuonFilter
		BCC = tree.BadChargedCandidateFilter
		eeBS = tree.eeBadScFilter
		nV = tree.NVtx
		EDCTP = tree.EcalDeadCellTriggerPrimitiveFilter

# MET Filters (all except for EcalDeadCellTriggerPrimitiveFilter
#		if not(gSTH == 1 and HBHEN == 1 and HBHEIN == 1 and BPFM == 1 and BCC == 1 and eeBS == 1 and EDCTP == 1 and nV > 0):
#			continue

		

	print("Total number of events is ")
	print nEvents


				# getattr is funky for methods. for a public variable of a class, getattr(obj, attr) works.
				# for a public function, needs getattr(obj,func)(args of func)
				# since JetsAK8[0].Pt() is a public function, the proper way to get that value using getattr is
				# getattr(JetsAK8[0],Pt)(), which we do here, but JetsAK8[0] is replaced by getattr(tree,JetsAK8)[0]

def addLoop():
	baseClass.loop = loop

