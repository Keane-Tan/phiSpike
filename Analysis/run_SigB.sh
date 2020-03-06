#!/bin/bash

# ./run_SigB.sh phiSigB

NAME=$1
MACRO="fsopt/$NAME.py"
OUT="$NAME.root"
OUTDIR="outputs/phiSpike/TriggerEff/SigBkg_Sens/OldCode/" # the output directory name

echo "Submitting jobs for $NAME"


for fileID in QCD16 QCD17 QCD18PRE QCD18POST TTJets16 WJets16 ZJets16 TTJets17 WJets17 ZJets17 TTJets18PRE WJets18PRE ZJets18PRE TTJets18POST WJets18POST ZJets18POST base

#Data16 QCD16 Data17 QCD17 Data18PRE QCD18PRE Data18POST QCD18POST TTJets16 WJets16 ZJets16 TTJets17 WJets17 ZJets17 TTJets18PRE WJets18PRE ZJets18PRE TTJets18POST WJets18POST ZJets18POST 

do
	if [ ! -d "$OUTDIR/$fileID" ]; then
		mkdir $OUTDIR/$fileID
	fi
	python main.py $MACRO $fileID inputTree_skims.txt $OUTDIR/$fileID $OUT 2 >& $OUTDIR/$fileID/$NAME.out &
	echo "Submitted  $fileID"
	sleep 10
done
echo Working...

wait

echo Finished.
