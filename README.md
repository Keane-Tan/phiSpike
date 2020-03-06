# phiSpike
Remove events that cause spikes in phi distributions.

This repository also contains codes that apply EcalDeadCellBoundaryEnergyFilter (a MET filter not in the recommended list) for 2016.

Everything starts with run_DMC.sh or similar bash files to generate the relevant root files. The output root files will be in the outputs folder. Some other things to take note of:

1) input_conf/inputRoot_fullRun2.py is where you can change the input root files used in the analysis. They are usually skim files.
2) macros folder contains scripts for doing different things in the analysis. In the scripts, you can decide which histograms to save and apply cuts.
3) outputs/phiSpike/plotScripts contains plot scripts used on the output root files.
