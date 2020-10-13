#!/bin/bash
# This script will update the ansbile vmware_dvswitch to allow creation
# of version 7.0.0 VDS

#sudo find / \( -path /var -o -path /mnt -o -path /run -o -path /proc \) -prune -false -o -name vmware_dvswitch.py
FILES="$(find $HOME -name vmware_dvswitch.py)"
for file in "$FILES"
do
    sed -i "s/'6.6.0']/'6.6.0', '7.0.0']/g" $file
done