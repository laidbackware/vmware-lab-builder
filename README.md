# vsphere-ansible-lab-builder
Build a nested vSphere lab with Ansible

## Description
You can use the ansible playbooks in this repo to build out nested ESXi hosts, deploy a vCenter and configure clusters. ESXi/vCenter 6.7 and 7.0 are supported.

# Dependencies
The following procedure has been developed on a debian based linux machine.<br/>

Infrastructure:
- A vSphere cluster with a manging vCenter.
- A datastore to host VMs of at least 200GB
- A control server which can contact the networks where VMs will be deployed.
- NTP available
Software versions:
- Ansible 2.10 or higher
- Linux tools `apt-get install libarchive-tools sshpass python3-pip git`
- Python modules `pip3 install pyvmomi ansible==2.10.* netaddr`
- Install [vSphere Automation SDK](https://github.com/vmware/vsphere-automation-sdk-python)
    `pip install --upgrade pip setuptools`
    `pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git`
- [ESXi OVA images](https://www.virtuallyghetto.com/nested-virtualization/nested-esxi-virtual-appliance)
- [vCenter ISO](https://my.vmware.com/en/group/vmware/downloads/info/slug/datacenter_cloud_infrastructure/vmware_vsphere/7_0)
- When installing TKGS
  - [VMware HA Proxy OVA](https://github.com/haproxytech/vmware-haproxy/releases/tag/v0.1.8)
  - [VyOS OVA](https://downloads.vyos.io/release/legacy/1.1.8/vyos-1.1.8-amd64.ova)

# Usage 
You must export the credentials to you existing vCenter as environmental variables along with the path which contains both the ESXi OVA and vCenter ISO.
```
export PARENT_VCENTER_USERNAME="administrator@vsphere.local" \
    PARENT_VCENTER_PASSWORD="VMware1!" \
    SOFTWARE_DIR="/home/matt/minio/vmware-products" 
```
## Local Usage
After cloneing the repo, you must update the relevant answerfile  yaml to point to your ova and iso file, plus change any IP addresses or credentials.<br/>
Currently the upstream vsphere community modules don't fully support all actions, so you must replace the the modules which ship with Ansible 2.10 with the ones provied. This only needs to be done after an install or upgrade of Ansible.
```
git clone --branch tkgs https://github.com/laidbackware/ansible-for-vsphere.git /tmp/ansible-for-vsphere \
cp -rf /tmp/ansible-for-vsphere/* /usr/local/lib/python3.*/dist-packages/ansible_collections/community/vmware/
```
Once all setup run:
```
ansible-playbook deploy.yml --extra-vars="@var-examples/minimal/answerfile-minimal.yml"
```

## Docker Usage 
After cloneing the repo, you must update the relevant answerfile  yaml to point to your ova and iso file, plus change any IP addresses or credentials.<br/>

```
docker run  --rm \
    --env PARENT_VCENTER_USERNAME=${PARENT_VCENTER_USERNAME} \
    --env PARENT_VCENTER_PASSWORD=${PARENT_VCENTER_PASSWORD} \
    --env SOFTWARE_DIR='/software_dir' \
    --env ANSIBLE_FORCE_COLOR='true' \
    --volume ${SOFTWARE_DIR}:/software_dir \
    --volume ${PWD}:/work \
    laidbackware/vsphere-ansible \
    ansible-playbook /work/deploy.yml \
        --extra-vars '@/work/var-examples/minimal/answerfile.yml'
```

## Destroying
When running the playbook, run destroy.yml instead. E.g. `ansible-playbook destroy.yml --extra-vars="@var-examples/minimal/answerfile-minimal.yml"`

# Docker Image Build
From the root of the repo. Note no-cache flag used to force builds to pickup any changes to the Ansible repo.
```
docker build --no-cache ./docker/ubuntu/. -t laidbackware/vsphere-ansible:latest
```

# Troubleshooting
The vCenter install can take a long time. You can check the progress by browsing to https://<vcenter IP>:5480. If the vCenter install fails, check the `vcsa-cli-installer.log` file which can be found in a created directory under /tmp.<br/>
To debug in docker, first enter the container with bash, then run the playbook. This way the vCenter build logs will be avaible after the failure.
```
docker run  -it --rm \
    --env PARENT_VCENTER_USERNAME=${PARENT_VCENTER_USERNAME} \
    --env PARENT_VCENTER_PASSWORD=${PARENT_VCENTER_PASSWORD} \
    --env SOFTWARE_DIR='/software_dir' \
    --env ANSIBLE_FORCE_COLOR='true' \
    --volume ${SOFTWARE_DIR}:/software_dir \
    --volume ${PWD}:/work \
    laidbackware/vsphere-ansible \
    /bin/bash

# The from the shell within the container
ansible-playbook /work/deploy.yml --extra-vars '@/work/answerfile-minimal.yml'
```

# Known issues/future plans
- The TKGS playbook is broken with vCenter  7.0U1 due to a bug with the vCenter not creating tag categories correctly.
- VMs are not currently deployed into a folder or resource pool on the parent vCenter.
- Only local datastores are used. In the future NFS support may be added.
- Include ability to add a content library with a remote data source