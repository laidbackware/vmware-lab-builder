# vsphere-ansible-lab-builder
Build a nested vSphere lab with Ansible

## Description
You can use the ansible playbooks in this repo to build out nested ESXi hosts, deploy a vCenter and configure clusters. ESXi/vCenter 6.7 and 7.0 are supported. The main design goal of this project is to be able to provide both opinionated deployment with few variables and to have the ability to fully customize the deployment.

# Dependencies
Infrastructure:
- A machine which is able to run docker that also has access to where the VMs will be deployed.
- A licensed vSphere cluster.
- A datastore to host VMs of at least 200GB.
- An NTP which is reachable by IP.
Software downloads:
- [ESXi OVA images](https://www.virtuallyghetto.com/nested-virtualization/nested-esxi-virtual-appliance)
- [vCenter ISO](https://my.vmware.com/en/group/vmware/downloads/info/slug/datacenter_cloud_infrastructure/vmware_vsphere/7_0)

## Tested versions
This release has been tested with the following components:
vSphere - 7.0.1c
ESXi nested OVA - 7.0U1
NSX-T - 3.1.0

# Usage 
Each deployment pattern has an opinionatend and a custom example. The idea of the opinionated deployment is that the user has to proide the minimum of configuration and the remainder of the options are calculated from this. Whereas the custom example has to have all sections built up by hand. Either of the examples types can be fully customized.<br/>

You must export the credentials to you existing vCenter as environmental variables along with the path on your local machine which contains the software listed above.
```
export PARENT_VCENTER_USERNAME="administrator@vsphere.local"
export PARENT_VCENTER_PASSWORD="VMware1!"
export SOFTWARE_DIR="/home/matt/minio/vmware-products" 
```

## Docker Usage 
After cloneing the repo, you should make a copy and update the relevant answerfile yaml, making sure to include your ova and iso file names, and to change any IP addresses and credentials.<br/>
Check the readme file in the example directory for any additional steps which may be needed for that solution.<br/>

The example below will deploy a single host and a vCenter, plus create a cluster with the minimum feature set. It should be run from the root of this repo and will copy the repo in as `/work`.
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
        --extra-vars '@/work/var-examples/base-vsphere/answerfile-1host-opinionated.yml'
```

## Destroying
To destroy run use destroy.yml. E.g. `ansible-playbook destroy.yml --extra-vars="@var-examples/vsphere-base/answerfile-1host-opinionated.yml"`

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
ansible-playbook /work/deploy.yml --extra-vars '@/work/<path>/<file>.yml'
```

# Roadmap
For solution specifc features, check the relevant example directory.
- Add output at the end showing all IP mappings
- Add roles for end to end NSX-T deployment
- Add module to deploy TKGS with NSX-T
- Add ability to deploy VMs to folders and resource pools on parent VC
- Add NFS datastore creation
- Add NFS server creation via Ubuntu VM
- Add more examples for different topologies
- Add support for VSAN configuration


# Docker Image Build
From the root of the repo. Note no-cache flag used to force builds to pickup any changes to the Ansible repo.
```
docker build --no-cache ./docker/ubuntu/. -t laidbackware/vsphere-ansible:latest
```

# Local Usage
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
ansible-playbook deploy.yml --extra-vars="@var-examples/base-vsphere/answerfile-1host-opinionated"
```