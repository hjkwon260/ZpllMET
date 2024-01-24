import os, sys
import json

ERA = sys.argv[1]

os.system("mkdir -p LIMIT/"+ERA+"/Logs_v1") # temp solution... xrdcp works differently
os.system("mkdir LIMIT/"+ERA+"/Plots")

input_datacard = 'combined_datacard.txt'


dic_limits={}

##-- set config --##
setting={}
with open('../config/Settrain.json') as json_file:
    data = json.load(json_file)
    setting=data
INPUTDIR = setting["INPUTDIR"]
VERSION = setting["VERSION"]
SIGNAL_MASSES = setting["ALL_MASSES"]

for mass in SIGNAL_MASSES:
	# Read in the file
	with open(input_datacard, 'r') as file :
		filedata = file.read()

	# Replace the target string
    filedata = filedata.replace('Zp-2500_CH-345', mass)

	# Write the file out again
	new_datacard = input_datacard.replace('.txt', '_new.txt')
	with open(new_datacard, 'w') as file:
		file.write(filedata)
	os.system("sleep 10s") # give some time file written completely

	os.system("combine -M AsymptoticLimits --run blind -t -1 "+new_datacard+" > LIMIT/"+ERA+"/Logs_v1/"+str(mass)+".log")

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
		print(lst_limits)
		dic_limits[m]=lst_limits

import json
with open('LIMIT/'+ERA+'/Logs_v1/limits_'+ERA+'.json', 'w') as fp:
    json.dump(dic_limits, fp)	
