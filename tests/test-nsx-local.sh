#!/bin/bash

set -eu

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

echo $script_dir

nsx_30_ova="nsx-unified-appliance-3.0.3.2.0.19603133.ova"
nsx_31_ova="nsx-unified-appliance-3.1.3.8.0.20532387.ova"
nsx_32_ova="nsx-unified-appliance-3.2.3.0.0.21703641.ova"
nsx_40_ova="nsx-unified-appliance-4.0.1.1.0.20598732.ova"

# export script_dir=$(pwd)

ansible-playbook $script_dir/deploy.yml --extra-vars "@$script_dir/var-examples/nsxt/opinionated.yml" \
  --extra-vars "nsxt_ova=${SOFTWARE_DIR}/${nsx_30_ova}" -vvv

ansible-playbook $script_dir/destroy.yml --extra-vars "@$script_dir/var-examples/nsxt/opinionated.yml"

ansible-playbook $script_dir/deploy.yml --extra-vars "@$script_dir/var-examples/nsxt/opinionated.yml" \
  --extra-vars "nsxt_ova=${SOFTWARE_DIR}/${nsx_31_ova}" -vvv

ansible-playbook $script_dir/destroy.yml --extra-vars "@$script_dir/var-examples/nsxt/opinionated.yml"

ansible-playbook $script_dir/deploy.yml --extra-vars "@$script_dir/var-examples/nsxt/opinionated.yml" \
  --extra-vars "nsxt_ova=${SOFTWARE_DIR}/${nsx_32_ova}" -vvv

ansible-playbook $script_dir/destroy.yml --extra-vars "@$script_dir/var-examples/nsxt/opinionated.yml"

ansible-playbook $script_dir/deploy.yml --extra-vars "@$script_dir/var-examples/nsxt/opinionated.yml" \
  --extra-vars "nsxt_ova=${SOFTWARE_DIR}/${nsx_40_ova}" -vvv

ansible-playbook $script_dir/destroy.yml --extra-vars "@$script_dir/var-examples/nsxt/opinionated.yml"