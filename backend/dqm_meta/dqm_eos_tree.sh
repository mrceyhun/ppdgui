#!/bin/sh
# Author     : Ceyhun Uzunoglu <ceyhunuzngl AT gmail dot com>

##H Runs tree command in DQM EOS parent directory to get all ROOT file names (includes run and dataset names) and their paths
##H File     : dqm_eos_tree.sh
##H Usage    : dqm_eos_tree.sh $base_dqm_eos_dir
##H Examples :
##H     - dqm_eos_tree.sh /eos/cms/store/group/comm_dqm/DQMGUI_data/Run202[2|3]/ downloads/tree.txt
##H     - dqm_eos_tree.sh /eos/cms/store/group/comm_dqm/DQMGUI_data/Run202*/
##H     - dqm_eos_tree.sh /eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/
##H

# help definition
if [ "$1" = "-h" ] || [ "$1" = "-help" ] || [ "$1" = "--help" ] || [ "$1" = "help" ] || [ "$1" = "" ]; then
    grep "^##H" <"$0" | sed -e "s,##H,,g"
    exit 1
fi

base_eos_dir=$1
outfile=$2

# Add slash to the end of base eos dir if not have
base_eos_dir="${base_eos_dir%/}/"

# -i: no dashes or tabs
# -f: full path
# -F: adds "/" to the end if its a directory
# -l: follow symbolic link like directory
# --noreport: no report of number of files/dirs in the output
# -I: ignore pattern
# grep : only names end with ".root", discards directories
tree -ifFl --noreport -I '*.dqminfo' "$base_eos_dir" | grep -E '\.root' >"$outfile"
