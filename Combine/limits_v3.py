import os, sys
import json
#
os.system("mkdir Logs_v1")
os.system("mkdir Plots")

input_datacard = 'datacard_ll_SR_v3.txt'
# input_root_file = '../Outputs/mm/shape_v1_dummyZp-2500_CH-345_v1.root'

dic_limits={}

##-- set config --##
setting={}
with open('../config/Settrain.json') as json_file:
    data = json.load(json_file)
    setting=data
INPUTDIR = setting["INPUTDIR"]
VERSION = setting["VERSION"]
SIGNAL_MASSES = setting["ALL_MASSES"]
# SIGNAL_MASSES = ['Zp-2500_CH-845']


for m in SIGNAL_MASSES:
	input_root_file = '../Outputs/SR/shape_v1_2803_equalpropv1'+m+'_v1.root'

	# Read in the file
	with open(input_datacard, 'r') as file :
		filedata = file.read()

	# Replace the target string
	filedata = filedata.replace('INPUT_ROOT_FILE', input_root_file)

	# Write the file out again
	new_datacard = input_datacard.replace('.txt', '_new.txt')
	with open(new_datacard, 'w') as file:
		file.write(filedata)
	os.system("sleep 10s") # give some time file written completely

	os.system("combine -M AsymptoticLimits --run blind -t -1 "+new_datacard+" > ./Logs_v1/"+str(m)+".log")

# 		# best fit
# 		os.system("text2workspace.py datacard_shape_mm_new.txt -m 800 -o workspace_"+d+".root")
# 		os.system("combine -M MultiDimFit workspace_"+d+".root -n "+d+" -m 200 --rMin -2 --rMax 2 --algo grid --points 30")
# 		os.system("python plot1DScan.py higgsCombine"+d+".MultiDimFit.mH200.root -o ./Plots/single_scan"+d)
# 		print("./Plots/single_scan"+d)
# 		print("//----Significance----//")
# 		os.system("combine -M Significance workspace_"+d+".root -m 200 --rMin -2 --rMax 2")
	##----- impact -----##
	if m == 'Zp-2500_CH-845':
		os.system("text2workspace.py "+new_datacard+" -m 800 -o "+new_datacard+".root")
		os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --doInitialFit")
		os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --doFits")
		os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --output impacts"+new_datacard+".json")
		os.system("plotImpacts.py -i impacts"+new_datacard+".json -o ./Plots/impacts"+m)



	with open("./Logs_v1/"+str(m)+".log", 'r') as file:
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
with open('Logs_v1/limits_v3.json', 'w') as fp:
    json.dump(dic_limits, fp)		
