#!/bin/bash

set -eu

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/.."

echo $script_dir

function run_playbook() {
  vars_file=$1
  action=$2
  echo "running $action for $vars_file"
  docker run --rm \
    --env PARENT_VCENTER_USERNAME=${PARENT_VCENTER_USERNAME} \
    --env PARENT_VCENTER_PASSWORD=${PARENT_VCENTER_PASSWORD} \
    --env SOFTWARE_DIR='/software_dir' \
    --env ANSIBLE_FORCE_COLOR='true' \
    --env NSXT_LICENSE_KEY=${NSXT_LICENSE_KEY:-na} \
    --env vars_file=${vars_file} \
    --env action=${action} \
    --volume ${SOFTWARE_DIR}:/software_dir \
    --volume ${script_dir}:/work \
    laidbackware/vmware-lab-builder:v1 \
    ansible-playbook /work/${action}.yml \
        --extra-vars '@/work/var-examples/${vars_file}.yml'

  return_code=$?
  if [[ $return_code -ne 0 ]]; then
    echo "$action failed for $vars_file"
    exit $return_code
  fi

  echo -e "\n\n############################################################################################"
  echo "$vars_file $action complete"
  echo -e "############################################################################################\n\n"
}

function run_test() {
  vars_file=$1
  
  run_playbook $vars_file deploy
  run_playbook $vars_file destroy
}

function test_opinionated_examples() {
  run_test base-vsphere/minimal-opinionated
  run_test nsxt/opinionated
  run_test tanzu/vsphere-vds/opinionated-1host-haproxy
  run_test tanzu/vsphere-nsxt/opinionated-1host
}

test_opinionated_examples