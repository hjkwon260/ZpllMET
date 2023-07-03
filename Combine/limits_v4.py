import os, sys
import json
#
os.system("mkdir Logs_v1")
os.system("mkdir Plots")

channel = sys.argv[1]

# input_datacard = 'datacard_ll_SR_v3.txt'
# input_datacard = 'datacard_allyears_channels.txt'
# input_datacard = 'datacard_ll_SR_smooth_v4.txt'
if channel == "combine":
	input_datacard = 'datacard_allyears_channels.txt'
else:
	input_datacard = 'datacard_ll_combine_v4.txt'


dic_limits={}

##-- set config --##
setting={}
with open('../config/Settrain.json') as json_file:
    data = json.load(json_file)
    setting=data
INPUTDIR = setting["INPUTDIR"]
VERSION = setting["VERSION"]
SIGNAL_MASSES = setting["ALL_MASSES"]
SIGNAL_MASSES = ['Zp-2500_CH-345']
# SIGNAL_MASSES = ['Zp-3300_CH-595']


for m in SIGNAL_MASSES:
	if channel == "combine":
		print('blah')
	# input_root_file_sree16 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/ee16/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcree16 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/ee16/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_sree17 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/ee17/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcree17 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/ee17/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_sree18 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/ee18/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcree18 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/ee18/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_srmm16 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/mm16/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcrmm16 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/mm16/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_srmm17 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/mm17/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcrmm17 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/mm17/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_srmm18 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/mm18/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcrmm18 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/mm18/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_srem16 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/em16/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcrem16 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/em16/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_srem17 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/em17/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcrem17 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/em17/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_srem18 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/em18/SR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	# input_root_file_ttcrem18 = '/eos/user/h/hkwon/Run2/Preselection/20230529deepCSV/Presel/em18/VR/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
	else:
		input_root_file_sr = '../SR/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		input_root_file_ttcr = '../VR/root_files/shape_v1_20230430wp80_ANv3'+m+'_v1.root'
		# input_root_file = "../Outputs/SR/shape_v1_20230529deepCSV_ANv3Zp-2500_CH-345_v1_smoothed.root"
		# input_root_file = '../Outputs/SRbak/shape_v1_20230430wp80_ANv3Zp-2500_CH-345_v1_smooted.root'

	# Read in the file
	with open(input_datacard, 'r') as file :
		filedata = file.read()

	# Replace the target string
	if channel == "combine":	
		print('blah')
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_16ee', input_root_file_sree16)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_16ee', input_root_file_ttcree16)
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_17ee', input_root_file_sree17)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_17ee', input_root_file_ttcree17)
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_18ee', input_root_file_sree18)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_18ee', input_root_file_ttcree18)
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_16mm', input_root_file_srmm16)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_16mm', input_root_file_ttcrmm16)
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_17mm', input_root_file_srmm17)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_17mm', input_root_file_ttcrmm17)
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_18mm', input_root_file_srmm18)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_18mm', input_root_file_ttcrmm18)
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_16em', input_root_file_srem16)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_16em', input_root_file_ttcrem16)
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_17em', input_root_file_srem17)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_17em', input_root_file_ttcrem17)
		# filedata = filedata.replace('INPUT_ROOT_FILE_SR_18em', input_root_file_srem18)
		# filedata = filedata.replace('INPUT_ROOT_FILE_TTCR_18em', input_root_file_ttcrem18)
	else:
		filedata = filedata.replace('INPUT_ROOT_FILE_SR', input_root_file_sr)
		filedata = filedata.replace('INPUT_ROOT_FILE_TTCR', input_root_file_ttcr)

	# Write the file out again
	new_datacard = input_datacard.replace('.txt', '_new.txt')
	with open(new_datacard, 'w') as file:
		file.write(filedata)
	os.system("sleep 10s") # give some time file written completely

	# os.system("combine -M AsymptoticLimits --run blind -t -1 "+new_datacard)
	os.system("combine -M AsymptoticLimits --run blind -t -1 "+new_datacard+" > ./Logs_v1/"+str(m)+".log")

# 		# best fit
# 		os.system("text2workspace.py datacard_shape_mm_new.txt -m 800 -o workspace_"+d+".root")
# 		os.system("combine -M MultiDimFit workspace_"+d+".root -n "+d+" -m 200 --rMin -2 --rMax 2 --algo grid --points 30")
# 		os.system("python plot1DScan.py higgsCombine"+d+".MultiDimFit.mH200.root -o ./Plots/single_scan"+d)
# 		print("./Plots/single_scan"+d)
# 		print("//----Significance----//")
# 		os.system("combine -M Significance workspace_"+d+".root -m 200 --rMin -2 --rMax 2")
	##----- impact -----##
	# if m == 'Zp-2500_CH-345' or m == 'Zp-2500_CH-845' or m == 'Zp-4100_CH-345':
	if m == 'Zp-2500_CH-345':
		os.system("text2workspace.py "+new_datacard+" -m 800 -o "+new_datacard+".root")
		os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --doInitialFit")
		os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --doFits")
		os.system("combineTool.py -M Impacts -d "+new_datacard+".root -m 200 --rMin -2 --rMax 2 --robustFit 1 -t -1 --expectSignal 0 --output impacts"+new_datacard+".json")
		os.system("plotImpacts.py -i impacts"+new_datacard+".json -o ./Logs_v1/impacts"+m)



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
with open('Logs_v1/limits_v4.json', 'w') as fp:
    json.dump(dic_limits, fp)		
