These are the steps to follow when running the codes for doing phi spike study.


# Getting the normalization values from the files with all the MET filters applied. These will the normalization values used for other files without EcalTP filter applied too.

1. Open rad_etaPhi.py and uncomment the lines (23-25, 45-51, 224-227) for finding normalization values.
2. Change the dirN to the directory containing the root files (MC and data) with all the MET filters applied.
3. Run
	python rad_etaPhi.py -b
* -b prevents ROOT canvas from popping up. The code runs faster that way.
4. Open the file phiSpike/NormalizationValues.txt
5. Copy and replace the lines of codes below the heading "Every 2D plots are normalized to the values below".
6. Comment out the lines for finding normalization values.
7. Run 
	python rad_etaPhi.py -b
8. Change dirN to the directory containing the root files without EcalTP or phi spike filters applied.
9. Run 
	python rad_etaPhi.py -b

* To get the 2D plots for files with phi spike filters applied, just run the command above after changer dirN to the appropriate directory.


# Getting the phi spike filter values.

1. Open the folder containing the root files without EcalTP or any phi Spike filter.
2. Look at the 1D plots and write down values that indicate a separation between low z values (where the majority of the events are) and the high z values (where there are very few events). 
3. Put these values in the appropriate lines under the heading "Identifying the eta and phi ranges with unusually high number of events".
4. Run
	python rad_etaPhi.py -b
5. Open the etaPhiRad.txt file, we will see the conditional statements representing the phi spike filters that are ready to be copied to the phiSpike.py macro.

* for block phi spike filters. run etaPhi.py instead, and open the etaPhi.txt file.

