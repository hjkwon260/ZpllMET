import os, sys
import json

ERA = sys.argv[1]
PART = sys.argv[2]

os.system("mkdir -p LIMIT/"+ERA+"/Logs_v1") # temp solution... xrdcp works differently
os.system("mkdir LIMIT/"+ERA+"/Plots")

input_datacard = 'combined_datacard.txt'


dic_limits={}

##-- set config --##
setting={}
with open('../../config/Settrain.json') as json_file:
    data = json.load(json_file)
    setting=data
INPUTDIR = setting["INPUTDIR"]
VERSION = setting["VERSION"]
SIGNAL_MASSES = setting["ALL_MASSES"]
if PART == "one":
	SIGNAL_MASSES = ["Zp-1700_CH-345", "Zp-1700_CH-595", "Zp-1700_CH-845", "Zp-2100_CH-345", "Zp-2100_CH-595", "Zp-2100_CH-845", "Zp-2500_CH-345", "Zp-2500_CH-595", "Zp-2500_CH-845", "Zp-2900_CH-345", "Zp-2900_CH-595"]
if PART == "two":
	SIGNAL_MASSES = ["Zp-2900_CH-845", "Zp-2900_CH-1095", "Zp-2900_CH-1345", "Zp-3300_CH-345", "Zp-3300_CH-595", "Zp-3300_CH-845", "Zp-3300_CH-1095", "Zp-3300_CH-1345", "Zp-3300_CH-1595", "Zp-3700_CH-345", "Zp-3700_CH-595"]
if PART == "three":
	SIGNAL_MASSES = ["Zp-3700_CH-845", "Zp-3700_CH-1095", "Zp-3700_CH-1345", "Zp-3700_CH-1595", "Zp-3700_CH-1845", "Zp-4100_CH-345", "Zp-4100_CH-595", "Zp-4100_CH-845", "Zp-4100_CH-1095", "Zp-4100_CH-1345", "Zp-4100_CH-1595", "Zp-4100_CH-1845"]

for mass in SIGNAL_MASSES:
	# Read in the file
	with open(input_datacard, 'r') as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('Zp-2500_CH-345', mass)
	# resolve segfault...
	filedata = filedata.replace('CMS_eff_trig', '#CMS_eff_trig')

	# Write the file out again
	new_datacard = input_datacard.replace('.txt', '_new.txt')
	with open(new_datacard, 'w') as file:
		file.write(filedata)
	os.system("sleep 10s") # give some time file written completely

	# os.system("combine -M AsymptoticLimits --run blind -t -1 "+new_datacard+" > LIMIT/"+ERA+"/Logs_v1/"+str(mass)+".log")
	os.system("combine -M AsymptoticLimits "+new_datacard+" > LIMIT/"+ERA+"/Logs_v1/"+str(mass)+".log")
	os.system("cp "+new_datacard+" LIMIT/"+ERA+"/Logs_v1/combined_datacard"+str(mass)+".txt)

	with open("LIMIT/"+ERA+"/Logs_v1/"+str(mass)+".log", 'r') as file:
		lst_limits=[]
		for line in file:
			if "Expected  2.5%: r <" in line:
				lst_limits.append(line.split(" ")[5].rstrip("\n"))
			if "Expected 16.0%: r <" in line:
				lst_limits.append(line.split(" ")[4].rstrip("\n"))
			if "Expected 50.0%: r <" in line:
				lst_limits.append(line.split(" ")[4].rstrip("\n"))
			if "Expected 84.0%: r <" in line:
				lst_limits.append(line.split(" ")[4].rstrip("\n"))
			if "Expected 97.5%: r <" in line:
				lst_limits.append(line.split(" ")[4].rstrip("\n"))
			if "Observed Limit: r <" in line:
				lst_limits.append(line.split(" ")[4].rstrip("\n"))

		print(lst_limits)
		dic_limits[mass]=lst_limits

		print(mass, lst_limits)

import json
with open('LIMIT/'+ERA+'/Logs_v1/limits_'+ERA+'.json', 'a') as fp:
    json.dump(dic_limits, fp)	
