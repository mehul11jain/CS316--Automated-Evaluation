assignment=$1 
low=$2 
upper=$3
RED='\033[1;91m'
GREEN='\033[1;92m'
CYAN='\033[1;36m'
NC='\033[0m'
# 1. Create ProgressBar function
# 1.1 Input is currentState($1) and totalState($2)
function ProgressBar {
# Process data
    let _progress=(${1}*100/${2}*100)/100
    let _done=(${_progress}*4)/10
    let _left=40-$_done
# Build progressbar string lengths
    _fill=$(printf "%${_done}s")
    _empty=$(printf "%${_left}s")

# 1.2 Build progressbar strings and print the ProgressBar line
# 1.2.1 Output example:                           
# 1.2.1.1 Progress : [########################################] 100%
printf "\rProgress : [${_fill// /#}${_empty// /-}] ${_progress}%%"

}

# Variables
_start=1

# This accounts as the "totalState" variable for the ProgressBar function
_end=$(($upper-$low + 1))
while [ $low -le $upper ];
do
    if [ -f "./$assignment/group$low.tar.gz" ];
    then 
        python3 run.py -tokens -error "group$low"        
        echo ""
        echo "====================================================================================="
        echo -e "${GREEN} Finished evaluating submission of group$low ${NC}"
        echo "====================================================================================="
        echo ""
    else
        echo ""
        echo "====================================================================================="
        echo -e "${RED}No file found for group$low${NC}"
        echo "====================================================================================="
        echo ""
    fi
    ProgressBar ${_start} ${_end}
    low=$(($low+1))
    _start=$(($_start+1))
done
