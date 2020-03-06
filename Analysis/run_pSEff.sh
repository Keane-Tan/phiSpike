#!/bin/bash

# ./run_pSEff.sh phiSpikeSignalEff

NAME=$1
MACRO="datamc/$NAME.py"
OUT="$NAME.root"
OUTDIR="outputs/phiSpike/TriggerEff/test/Efficiencies/SignalEff/phiSpike_leadsublead/" # the output directory name

echo "Submitting jobs for $NAME"


for fileID in base

#z05 z06 z07 z08 z09 z10 z11 z12 z13 z14 z15 z16 z17 z18 z19 z20 z21 z22 z23 z24 z25 z26 z27 z28 z29 base z31 z32 z33 z34 z35 z36 z37 z38 z39 z40 z41 z42 z43 z44 z45 d00 d01 d05 d10 d30 d40 d50 d60 d70 d80 d90 r00 r01 r02 r04 r05 r06 r07 r08 r09 r10 ad217 ad216 adh adl
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
