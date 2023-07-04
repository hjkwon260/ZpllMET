import os, sys
import json

ERA = sys.argv[1]

os.system("mkdir -p LIMIT/LIMIT/"+ERA+"/Logs_v1") # temp solution... xrdcp works differently
os.system("mkdir LIMIT/LIMIT/"+ERA+"/Plots")

# input_datacard = 'datacard_ll_SR_v3.txt'
# input_datacard = 'datacard_allyears_channels.txt'
# input_datacard = 'datacard_ll_SR_smooth_v4.txt'
if ERA == "all":
	input_datacard = 'datacards/datacard_allyears_channels.txt'
elif ERA == "mm" or ERA == "ee" or ERA == "em":
	input_datacard = 'datacards/datacard_allyears.txt'	
else:
	input_datacard = 'datacards/datacard_ll_combine_v4.txt'


dic_limits={}

##-- set config --##
setting={}
with open('../config/Settrain.json') as json_file:
    data = json.load(json_file)
    setting=data
INPUTDIR = setting["INPUTDIR"]
VERSION = setting["VERSION"]
SIGNAL_MASSES = setting["ALL_MASSES"]
# SIGNAL_MASSES = ['Zp-2500_CH-345']
# SIGNAL_MASSES = ['Zp-3300_CH-595']


for m in SIGNAL_MASSES:
	if ERA == "all":
		input_root_file_sr_mm16 = '../SR/mm16/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_mm16 = '../VR/mm16/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_mm17 = '../SR/mm17/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_mm17 = '../VR/mm17/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_mm18 = '../SR/mm18/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_mm18 = '../VR/mm18/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_ee16 = '../SR/ee16/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_ee16 = '../VR/ee16/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_ee17 = '../SR/ee17/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_ee17 = '../VR/ee17/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_ee18 = '../SR/ee18/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_ee18 = '../VR/ee18/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_em16 = '../SR/em16/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_em16 = '../VR/em16/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_em17 = '../SR/em17/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_em17 = '../VR/em17/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_em18 = '../SR/em18/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_em18 = '../VR/em18/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	elif ERA == "mm" or ERA == "ee" or ERA == "em":
		input_root_file_sr_16 = '../SR/16/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_16 = '../VR/16/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_17 = '../SR/17/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_17 = '../VR/17/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
		input_root_file_sr_18 = '../SR/18/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr_18 = '../VR/18/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'		
	else:
		input_root_file_sr = '../SR/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr = '../VR/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		# input_root_file_sr = "../Outputs/SR/shape_v1_20230529deepCSV_ANv3Zp-2500_CH-345_v1_smoothed.root"
		# input_root_file_ttcr = "../Outputs/SR/shape_v1_20230529deepCSV_ANv3Zp-2500_CH-345_v1_smoothed.root"
		# input_root_file = '../Outputs/SRbak/shape_v1_20230430wp80_ANv3Zp-2500_CH-345_v1_smooted.root'

	# Read in the file
	with open(input_datacard, 'r') as file :
		filedata = file.read()

	# Replace the target string
	if ERA == "all":	
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_16ee', input_root_file_sr_ee16)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_16ee', input_root_file_ttcr_ee16)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_17ee', input_root_file_sr_ee17)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_17ee', input_root_file_ttcr_ee17)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_18ee', input_root_file_sr_ee18)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_18ee', input_root_file_ttcr_ee18)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_16mm', input_root_file_sr_mm16)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_16mm', input_root_file_ttcr_mm16)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_17mm', input_root_file_sr_mm17)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_17mm', input_root_file_ttcr_mm17)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_18mm', input_root_file_sr_mm18)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_18mm', input_root_file_ttcr_mm18)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_16em', input_root_file_sr_em16)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_16em', input_root_file_ttcr_em16)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_17em', input_root_file_sr_em17)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_17em', input_root_file_ttcr_em17)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_18em', input_root_file_sr_em18)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_18em', input_root_file_ttcr_em18)
	elif ERA == "mm" or ERA == "ee" or ERA == "em":
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_16', input_root_file_sr_16)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_16', input_root_file_ttcr_16)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_17', input_root_file_sr_17)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_17', input_root_file_ttcr_17)
		filedata = filedata.replace('INPUT_ROOT_FILE_SR_18', input_root_file_sr_18)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_18', input_root_file_ttcr_18)
	else:
		filedata = filedata.replace('INPUT_ROOT_FILE_SR', input_root_file_sr)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR', input_root_file_ttcr)

	# Write the file out again
	new_datacard = input_datacard.replace('.txt', '_new.txt')
	with open(new_datacard, 'w') as file:
		file.write(filedata)
	os.system("sleep 10s") # give some time file written completely

	# os.system("combine -M AsymptoticLimits --run blind -t -1 "+new_datacard)
	os.system("combine -M AsymptoticLimits --run blind -t -1 "+new_datacard+" > LIMIT/LIMIT/"+ERA+"/Logs_v1/"+str(m)+".log")

# 		# best fit
# 		os.system("text2workspace.py datacard_shape_mm_new.txt -m 800 -o workspace_"+d+".root")
# 		os.system("combine -M MultiDimFit workspace_"+d+".root -n "+d+" -m 200 --rMin -2 --rMax 2 --algo grid --points 30")
# 		os.system("python plot1DScan.py higgsCombine"+d+".MultiDimFit.mH200.root -o ./Plots/single_scan"+d)
# 		print("./Plots/single_scan"+d)
# 		print("//----Significance----//")
# 		os.system("combine -M Significance workspace_"+d+".root -m 200 --rMin -2 --rMax 2")
	##----- impact -----##
	# if m == 'Zp-2500_CH-345' or m == 'Zp-2500_CH-845' or m == 'Zp-4100_CH-345':
	# if m == 'Zp-2500_CH-345':
	# 	os.system("text2workspace.py "+new_datacard+" -m 800 -o "+new_datacard+".root")
	# 	os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --doInitialFit")
	# 	os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --doFits")
	# 	os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --output impacts"+new_datacard+".json")
	# 	os.system("plotImpacts.py -i impacts"+new_datacard+".json -o LIMIT/LIMIT/"+ERA+"/Plots/impacts"+m)



	with open("LIMIT/LIMIT/"+ERA+"/Logs_v1/"+str(m)+".log", 'r') as file:
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
with open('LIMIT/LIMIT/'+ERA+'/Logs_v1/limits_v4.json', 'w') as fp:
    json.dump(dic_limits, fp)	