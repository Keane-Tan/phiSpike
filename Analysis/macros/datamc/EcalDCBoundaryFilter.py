from analysisBase import baseClass
import ROOT as rt
import tdrstyle
from array import array
from EventListFilter import *

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

	# lists of EcalDCBoundaryFilter for 2016
	filter_dir = 'macros/datamc/EcalDCBoundary/lists/'

	if "Data16" in self.fileID:
		filter_files = [filter_dir+'Run2016B_ver2-Nano1June2019_ver2-v2_JetHT_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Run2016C-Nano1June2019-v1_JetHT_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Run2016D-Nano1June2019-v1_JetHT_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Run2016E-Nano1June2019-v1_JetHT_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Run2016F-Nano1June2019-v1_JetHT_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Run2016G-Nano1June2019-v1_JetHT_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Run2016H-Nano1June2019-v1_JetHT_EcalDeadCellBoundaryEnergyFilterList.txt']
		EcalDCBoundaryEFilter  = EventListFilter(filter_files)

	elif "QCD16" in self.fileID:
		filter_files = [filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt',filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_1000to1400_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_120to170_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_1400to1800_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_170to300_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_1800to2400_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_2400to3200_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_300to470_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_3200toInf_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_470to600_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_600to800_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_800to1000_TuneCUETP8M1_13TeV_pythia8_ext1_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8_EcalDeadCellBoundaryEnergyFilterList.txt', filter_dir+'Summer16v5-Nano1June2019_QCD_Pt_80to120_TuneCUETP8M1_13TeV_pythia8_ext2_EcalDeadCellBoundaryEnergyFilterList.txt']
		EcalDCBoundaryEFilter = EventListFilterMC(filter_files)

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

	# list of branches to plot
	plotDict = {#key = var name, value = [varType, nBins, binLow, binHigh, title]
				# varType can be "s" - single value (ie 'MET')
	'AK8jet[0]_etaphi':["s",50,-2.4,2.4,50,-3.5,3.5,self.fileID+";AK8jet_0_etaphi; Events"],
	'AK8jet[1]_etaphi':["s",50,-2.4,2.4,50,-3.5,3.5,self.fileID+";AK8jet_1_etaphi; Events"],
	'AK4jet[0]_etaphi':["s",50,-2.4,2.4,50,-3.5,3.5,self.fileID+";AK4jet_0_etaphi; Events"],
	'AK4jet[1]_etaphi':["s",50,-2.4,2.4,50,-3.5,3.5,self.fileID+";AK4jet_1_etaphi; Events"],
	'MET':["s",100,200,metx*1.01,self.fileID+";MET; Events"],
	'METPhi':["s",100,-Phix*1.01,Phix*1.01,self.fileID+";#phi(MET); Events"],
	'AK8jet[0]_phi':["s",100,-Phix*1.01,Phix*1.01,self.fileID+";#phi(j_0); Events"],
	'AK8jet[1]_phi':["s",100,-Phix*1.01,Phix*1.01,self.fileID+";#phi(j_1); Events"],
	'AK4jet[0]_phi':["s",100,-Phix*1.01,Phix*1.01,self.fileID+";#phi(j_0); Events"],
	'AK4jet[1]_phi':["s",100,-Phix*1.01,Phix*1.01,self.fileID+";#phi(j_1); Events"]
	}
	branchList = tree.GetListOfBranches()
	branchListNames = []
	for thing in branchList:
		branchListNames.append(thing.GetName())
	tree.SetBranchStatus("*",0)
	tree.SetBranchStatus("RunNum" ,1)
	tree.SetBranchStatus("LumiBlockNum" ,1)
	tree.SetBranchStatus("EvtNum" ,1)
	tree.SetBranchStatus("GenJets" ,1)
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
	histDict = {}

	for plotVar, histSpecs in plotDict.items():
		if len(histSpecs) > 6:
			histDict[plotVar] = self.makeTH2F(plotVar+"_"+self.fileID,histSpecs[7],histSpecs[1],histSpecs[2],histSpecs[3],histSpecs[4],histSpecs[5],histSpecs[6]) # 2D plots
		else:
			histDict[plotVar] = self.makeTH1F(plotVar+"_"+self.fileID,histSpecs[4],histSpecs[1],histSpecs[2],histSpecs[3]) # 1D plots
	
	WtotE = 0
	totE = 0
	CtotE = 0
	tot_EBoundaryPass = 0
	tot_ETPFilter = 0
	tot_both = 0
	
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

# MET Filters (all except for EcalDeadCellTriggerPrimitiveFilter
		if not(gSTH == 1 and HBHEN == 1 and HBHEIN == 1 and BCC == 1 and eeBS == 1 and BPFM==1 and nV > 0):
			continue
		
		pass_Boundary = True

# Apply EcalDeadCellBoundaryEnergyFilter
		if "Data16" in self.fileID:
			pass_Boundary = EcalDCBoundaryEFilter.CheckEvent(tree.RunNum, tree.LumiBlockNum, tree.EvtNum)
		elif "QCD16" in self.fileID:
			pass_Boundary = EcalDCBoundaryEFilter.CheckEvent(tree.RunNum, tree.LumiBlockNum, tree.EvtNum, int(tree.GenJets[0].Pt()))

# Counting Events that Pass the EcalDeadCell* Filters
		if pass_Boundary: tot_EBoundaryPass += 1
		if EDCTP == 1: tot_ETPFilter += 1
		if pass_Boundary and EDCTP == 1: tot_both += 1

		if "Data16" in self.fileID:
			if not pass_Boundary: continue
		elif "QCD16" in self.fileID:
			if not pass_Boundary: continue

#		Keeping track of the number of events
		WtotE += weight*lumi
		totE += 1
		CWeight = weight*lumi*tEff
		CtotE += CWeight

# 		Filling histograms		
		histDict['AK4jet[0]_etaphi'].Fill(Jets[0].Eta(),Jets[0].Phi(),CWeight)
		histDict['AK4jet[1]_etaphi'].Fill(Jets[1].Eta(),Jets[1].Phi(),CWeight)
		histDict['AK8jet[0]_etaphi'].Fill(FJets[0].Eta(),FJets[0].Phi(),CWeight)
		histDict['AK8jet[1]_etaphi'].Fill(FJets[1].Eta(),FJets[1].Phi(),CWeight)
		if MET > metx:
			histDict['MET'].Fill(metx,CWeight)
		else:
			histDict['MET'].Fill(MET,CWeight)

		histDict['METPhi'].Fill(METPhi,CWeight)
		histDict['AK4jet[0]_phi'].Fill(Jets[0].Phi(),CWeight)
		histDict['AK4jet[1]_phi'].Fill(Jets[1].Phi(),CWeight)
		histDict['AK8jet[0]_phi'].Fill(FJets[0].Phi(),CWeight)
		histDict['AK8jet[1]_phi'].Fill(FJets[1].Phi(),CWeight)

	print "Passed EcalDeadCellBoundaryEnergyFilter = "+str(tot_EBoundaryPass)
	print "Passed EcalDeadCellTriggerPrimitiveFilter = "+str(tot_ETPFilter)
	print "Passed both = "+str(tot_both)

	print("Number of events:")
	print totE			
	print("Weighted number of events:")
	print WtotE
	print("Weighted number of events with trigger efficiency:")
	print CtotE

def addLoop():
	baseClass.loop = loop

