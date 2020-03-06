from analysisBase import baseClass
import ROOT as rt
import tdrstyle
from array import array
from EventListFilter import *

rt.gROOT.SetBatch(True)
rt.gStyle.SetOptTitle(1)
tdrstyle.setTDRStyle()

def loop(self):

	def vetoPhiSpike(etaHSL,phiHSL,rad,ai,bi):
		for iep in range(len(etaHSL)):
 			if ((etaHSL[iep] - ai)**2 + (phiHSL[iep] - bi)**2 < rad):
				return True
				break

	def GetCorr(var,fun):        # returns trigger efficiency; var = MTAK8, fun = fun16, fun17, or fun18
		if(var > fun.GetXmax()):
			var = fun.GetXmax()
		if(var < fun.GetXmin()):
			var = fun.GetXmin()
		return fun.Eval(var)

	# lists of EcalDCBoundaryFilter for 2016
	filter_dir = 'macros/datamc/EcalDCBoundary/lists/'

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
	tree.SetBranchStatus("MET",1)
	tree.SetBranchStatus("METPhi",1)
	tree.SetBranchStatus("MT_AK8",1)
	tree.SetBranchStatus("NVtx",1)	
	tree.SetBranchStatus("Muons_MiniIso",1)
	tree.SetBranchStatus("NElectrons",1)
	tree.SetBranchStatus("globalSuperTightHalo2016Filter",1)
	tree.SetBranchStatus("HBHENoiseFilter",1)
	tree.SetBranchStatus("HBHEIsoNoiseFilter",1)
	tree.SetBranchStatus("BadPFMuonFilter",1)
	tree.SetBranchStatus("BadChargedCandidateFilter",1)
	tree.SetBranchStatus("eeBadScFilter",1)

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

	print self.fileID

	eff16 = 0
	eff17 = 0
	eff18PRE = 0
	eff18POST = 0
	tru_nEvents = 0
		
	for iEvent in range(nEvents):
		if iEvent%1000 == 0:
			print("Event: " + str(iEvent) + "/" + str(nEvents))
		tree.GetEvent(iEvent)

		if (("Jets" in self.fileID) or ("QCD" in self.fileID)): # or ("ST1" in self.fileID)): # Bkg MC get tree weight, data and signal MC get weight == 1		
			weight = (tree.Weight)*(tree.puWeightNew)
		else: 
			weight = 1.
		
		# Applying HEM Veto
		if "18" in self.fileID:
			if (("PRE" in self.fileID) and ("Data" in self.fileID) and (tree.RunNum >= 319077)):
				continue
			elif "POST" in self.fileID:
				if ( ( ("Data" in self.fileID) and (tree.RunNum < 319077) ) or (tree.HEMOptVetoFilter == 0) ):
					continue

		# Calculating trigger efficiency
		MTAK8 = tree.MT_AK8
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

		CWeight = weight*lumi*tEff
		tru_nEvents += 1.

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

# MT window
#		lowMTlim = 2000.0
#		highMTlim = 4000.0

#		if lowMTlim > tree.MT_AK8 or tree.MT_AK8 > highMTlim:
#			continue


# MET Filters 
		if not(gSTH == 1 and HBHEN == 1 and HBHEIN == 1 and BPFM == 1 and BCC == 1 and eeBS == 1 and nV > 0):
			continue

#		eff16 += 1.
#			eff17 += 1.
#			eff18PRE += 1.
#			eff18POST += 1.

# Apply EcalDeadCellBoundaryEnergyFilter to Data and QCD
#		pass_Boundary = True

#		if "Data16" in self.fileID:
#			pass_Boundary = EcalDCBoundaryEFilter.CheckEvent(tree.RunNum, tree.LumiBlockNum, tree.EvtNum)
#		elif "QCD16" in self.fileID:
#			pass_Boundary = EcalDCBoundaryEFilter.CheckEvent(tree.RunNum, tree.LumiBlockNum, tree.EvtNum, int(tree.GenJets[0].Pt()))

#		if "Data16" in self.fileID:
#			if not pass_Boundary: continue
#		elif "QCD16" in self.fileID:
#			if not pass_Boundary: continue

#		eff16 += CWeight

## phi spike filters
		rad = 0.028816 # half the length of the diagonal of the eta-phi rectangular cell
		rad = rad * 0.35 # the factor of 0.35 was optimized from the signal vs. background sensitivity study

		# hot spots for leading jets
		eta16lead = [0.048,0.24,1.488,1.584,-1.008]
		phi16lead = [-0.35,-0.35,-0.77,-0.77,-1.61]

		eta17lead = [0.144,1.488,1.488,1.584,-0.624]
		phi17lead = [-0.35,-0.77,-0.63,-0.77,0.91]

		eta18lead = [1.488,1.488,1.584]
		phi18lead = [-0.77,-0.63,-0.77] 

		# hot spots for subleading jets
		eta16 = [-1.2,-0.912,-0.912,-0.816,-0.72,-0.72,-0.528,-0.432,-0.336,-0.24,-0.24,-0.144,-0.144,-0.048,0.144,
0.912,0.912,1.008,1.296,-1.584,-0.816,-0.72,-0.144,-0.048,-0.048,0.048,1.104,1.488]
		phi16 = [-1.19,2.03,3.01,-1.75,-2.17,-0.77,2.73,2.73,0.21,0.07,0.21,-2.59,0.77,0.91,1.75,1.75,2.87,0.63,
-0.49,0.63,1.47,-2.31,0.07,-2.59,0.77,0.91,-3.15,2.73]

		eta17 = [-0.912,-0.912,-0.816,-0.72,-0.528,-0.336,-0.24,-0.24,-0.144,-0.144,-0.048,0.144,0.912,0.912,1.008,
-1.2,-0.72,-0.72,-0.432,0.336,0.624,1.104,1.296]
		phi17 = [2.03,3.01,-1.75,-0.77,2.73,0.21,0.07,0.21,-2.59,0.77,0.91,1.75,1.75,2.87,0.63,-1.19,-2.31,-2.17,
2.73,-0.77,-0.77,-3.15,-0.49]

		eta18PRE = [-1.584,-1.2,-0.912,-0.912,-0.816,-0.816,-0.72,-0.72,-0.528,-0.432,-0.336,-0.24,-0.24,-0.144,-0.144,
-0.144,-0.048,-0.048,0.144,0.912,0.912,1.008,1.296,-0.72,1.104,1.488,1.776]
		phi18PRE = [0.63,-1.19,2.03,3.01,-1.75,-0.77,-2.17,-0.77,2.73,2.73,0.21,0.07,0.21,-2.59,0.07,0.77,0.77,0.91,
1.75,1.75,2.87,0.63,-0.49,-2.31,-3.15,-0.21,0.77]

		eta18POST = [-1.2,-0.912,-0.912,-0.816,-0.72,-0.528,-0.336,-0.24,-0.24,-0.144,-0.144,-0.048,0.144,0.912,0.912,
1.008,1.296,-1.584,-0.816,-0.72,-0.72,-0.432,-0.144,-0.048,1.104,1.488,1.776]
		phi18POST = [-1.19,2.03,3.01,-1.75,-0.77,2.73,0.21,0.07,0.21,-2.59,0.77,0.91,1.75,1.75,2.87,0.63,-0.49,0.63,
-0.77,-2.31,-2.17,2.73,0.07,0.77,-3.15,-0.21,0.77]

		# 2016
		if vetoPhiSpike(eta16,phi16,rad,Jets[1].Eta(),Jets[1].Phi()) or vetoPhiSpike(eta16lead,phi16lead,rad,Jets[0].Eta(),Jets[0].Phi()):
			eff16 += 0
		else:
			#eff16 += CWeight # background
			eff16 += 1. # signal

		# 2017
		if vetoPhiSpike(eta17,phi17,rad,Jets[1].Eta(),Jets[1].Phi()) or vetoPhiSpike(eta17lead,phi17lead,rad,Jets[0].Eta(),Jets[0].Phi()):
			eff17 += 0
		else:
			eff17 += 1.

		# 2018PRE
		if vetoPhiSpike(eta18PRE,phi18PRE,rad,Jets[1].Eta(),Jets[1].Phi()) or vetoPhiSpike(eta18lead,phi18lead,rad,Jets[0].Eta(),Jets[0].Phi()):
			eff18PRE += 0
		else:
			eff18PRE += 1.

		# 2018POST
		if vetoPhiSpike(eta18POST,phi18POST,rad,Jets[1].Eta(),Jets[1].Phi()) or vetoPhiSpike(eta18lead,phi18lead,rad,Jets[0].Eta(),Jets[0].Phi()):
			eff18POST += 0
		else:
			eff18POST += 1.

	print eff16
	print tru_nEvents
	print eff16/tru_nEvents
	print eff17/tru_nEvents
	print eff18PRE/tru_nEvents
	print eff18POST/tru_nEvents
				# getattr is funky for methods. for a public variable of a class, getattr(obj, attr) works.
				# for a public function, needs getattr(obj,func)(args of func)
				# since JetsAK8[0].Pt() is a public function, the proper way to get that value using getattr is
				# getattr(JetsAK8[0],Pt)(), which we do here, but JetsAK8[0] is replaced by getattr(tree,JetsAK8)[0]

def addLoop():
	baseClass.loop = loop

