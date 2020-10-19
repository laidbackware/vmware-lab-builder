#!/bin/bash
# This script will update the ansbile vmware_dvswitch to allow creation
# of version 7.0.0 VDS

# run as user check in homedir, else check everywhere
if [ "$EUID" -ne 0 ]; then
    FILES="$(find $HOME -name vmware_dvswitch.py)"
else
    FILES="$(find / \( -path /var -o -path /mnt -o -path /run -o -path /proc \) -prune -false -o -name vmware_dvswitch.py)"
fi

for file in "$FILES"
do
    sed -i "s/'6.6.0']/'6.6.0', '7.0.0']/g" $file
done