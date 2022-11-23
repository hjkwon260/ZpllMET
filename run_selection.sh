#!bin/bash
script=$1
dir_date=$2 # without white space
# declare -a eras=("ee16pre" "mm16pre" "em16pre" "ee16post" "mm16post" "em16post" "ee17" "mm17" "em17" "ee18" "mm18" "em18")
# declare -a eras=("ee16post" "mm16post" "em16post" "ee17" "mm17" "em17" "ee18" "mm18" "em18")
declare -a eras=("ee17" "mm17" "em17" "ee18" "mm18" "em18")
i=0

jupyter nbconvert --to python ${script}.ipynb
for era in "${eras[@]}"
do
	python ${script}.py $era $dir_date
	if [ $? -eq 0 ]
	then
	  echo "Successfully executed script"
	  let "i+=1"
	else
	  # Redirect stdout from echo command to stderr.
	  echo $?
	  echo "Script exited with error."
	  break 
	fi
done
if [ $? -eq 0 ]
then
  echo "Jobs finished"
  echo "Move to wep"
  python MoveToWeb.py $dir_date
  # beep
fi
echo $i
