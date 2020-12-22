# vsphere-ansible-lab-builder
Build a nested vSphere lab with Ansible

## Description
You can use the ansible playbooks in this repo to build out nested ESXi hosts, deploy a vCenter and configure clusters. ESXi/vCenter 6.7 and 7.0 are supported.

# Dependencies
Infrastructure:
- A machine which is able to run docker that also has access to where the VMs will be deployed.
- A licensed vSphere cluster.
- A datastore to host VMs of at least 200GB.
- An NTP which is reachable by IP.
Software downoads:
- [ESXi OVA images](https://www.virtuallyghetto.com/nested-virtualization/nested-esxi-virtual-appliance)
- [vCenter ISO](https://my.vmware.com/en/group/vmware/downloads/info/slug/datacenter_cloud_infrastructure/vmware_vsphere/7_0)
- When installing TKGS
  - [VMware HA Proxy OVA](https://github.com/haproxytech/vmware-haproxy/releases/tag/v0.1.8)
  - [VyOS OVA](https://downloads.vyos.io/release/legacy/1.1.8/vyos-1.1.8-amd64.ova)

# Usage 
You must export the credentials to you existing vCenter as environmental variables along with the path on your local machine which contains the software listed above.
```
export PARENT_VCENTER_USERNAME="administrator@vsphere.local"
export PARENT_VCENTER_PASSWORD="VMware1!"
export SOFTWARE_DIR="/home/matt/minio/vmware-products" 
```

## Docker Usage 
After cloneing the repo, you must update the relevant answerfile yaml include your ova and iso file names, and change any IP addresses or credentials.<br/>
Check the readme file in the example directory for any additional steps which may be needed for that solution.<br/>

The example below will deploy a single host and a vCenter, plus create a cluster with the minimum feature set.
```
docker run --rm \
    --env PARENT_VCENTER_USERNAME=${PARENT_VCENTER_USERNAME} \
    --env PARENT_VCENTER_PASSWORD=${PARENT_VCENTER_PASSWORD} \
    --env SOFTWARE_DIR='/software_dir' \
    --env ANSIBLE_FORCE_COLOR='true' \
    --volume ${SOFTWARE_DIR}:/software_dir \
    --volume ${PWD}:/work \
    laidbackware/vsphere-ansible \
    ansible-playbook /work/deploy.yml \
        --extra-vars '@/work/var-examples/vsphere-base/answerfile-1host-opinionated.yml'
```

## Destroying
To destroy run use destroy.yml. E.g. `ansible-playbook destroy.yml --extra-vars="@var-examples/vsphere-base/answerfile-1host-opinionated.yml"`

# Docker Image Build
From the root of the repo. Note no-cache flag used to force builds to pickup any changes to the Ansible repo.
```
docker build --no-cache ./docker/ubuntu/. -t laidbackware/vsphere-ansible:latest
```

# Troubleshooting
The vCenter install can take a long time. You can check the progress by browsing to https://<vcenter IP>:5480. If the vCenter install fails, check the `vcsa-cli-installer.log` file which can be found in a created directory under /tmp.<br/>
To debug in docker, first enter the container with bash, then run the playbook. This way the vCenter build logs will be avaible after the failure.
```
# This command will start a bash shell within the container
docker run  -it --rm \
    --env PARENT_VCENTER_USERNAME=${PARENT_VCENTER_USERNAME} \
    --env PARENT_VCENTER_PASSWORD=${PARENT_VCENTER_PASSWORD} \
    --env SOFTWARE_DIR='/software_dir' \
    --env ANSIBLE_FORCE_COLOR='true' \
    --volume ${SOFTWARE_DIR}:/software_dir \
    --volume ${PWD}:/work \
    laidbackware/vsphere-ansible \
    /bin/bash

# Then the playbook can be triggered
ansible-playbook /work/deploy.yml --extra-vars '@/work/answerfile-minimal.yml'
```

# Known issues/future plans
- VMs are not currently deployed into a folder or resource pool on the parent vCenter.
- Only local datastores are used. In the future NFS support may be added.

## Local Usage
At the current time it's advised against trying to run locally as modifications are needed to the vSphere community modules, which have pull requests pending.<br/>
After cloneing the repo, you must update the relevant answerfile  yaml to point to your ova and iso file, plus change any IP addresses or credentials.<br/>
Currently the upstream vsphere community modules don't fully support all actions, so you must replace the the modules which ship with Ansible 2.10 with the ones provied. This only needs to be done after an install or upgrade of Ansible.
Software dependencies for Linux:
- Ansible 2.10 or higher
- Linux tools `apt-get install libarchive-tools sshpass python3-pip git`
- Python modules `pip3 install pyvmomi ansible==2.10.* netaddr`
- Install [vSphere Automation SDK](https://github.com/vmware/vsphere-automation-sdk-python)
    `pip install --upgrade pip setuptools`
    `pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git`
```
git clone --branch tkgs https://github.com/laidbackware/ansible-for-vsphere.git /tmp/ansible-for-vsphere
# Below is an example which works for Ubuntu, the dist-packages location may differ for other distros.
cp -rf /tmp/ansible-for-vsphere/* /usr/local/lib/python3.*/dist-packages/ansible_collections/community/vmware/
# In the vsphere collection has been previously added via ansible-galaxy, the directory should be removed.
```
Once all setup run the playbooks can be run locally:
```
ansible-playbook deploy.yml --extra-vars="@var-examples/vsphere-base/answerfile-1host-opinionated"
```