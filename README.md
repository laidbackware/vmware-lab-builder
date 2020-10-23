# vsphere-ansible-lab-builder
Build a nested vSphere lab with Ansible

## Description
You can use the ansible playbooks in this repo to build out nested ESXi hosts, deploy a vCenter and configure clusters. ESXi/vCenter 6.7 and 7.0 are supported.

# Dependencies
The following procedure has been developed on a debian based linux machine.<br/>
This process will build a vCenter and 1 or more clusters, with nested ESXi hosts.<br/> 
Infrastructure:
- A vSphere cluster with a manging vCenter.
- A datastore to host VMs of at least 200GB
- A control server which can contact the networks when VMs will be deployed.
- NTP available
Software versions:
- Ansible 2.10 or higher
- Linux tools `apt-get install xorriso sshpass python-pip git`
- Python modules `pip3 install pyvmomi`
- Install [vSphere Automation SDK](https://github.com/vmware/vsphere-automation-sdk-python)
    `pip install --upgrade pip setuptools`
    `pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git`
- [ESXi OVA images](https://www.virtuallyghetto.com/nested-virtualization/nested-esxi-virtual-appliance)
- [vCenter ISO](https://my.vmware.com/en/group/vmware/downloads/info/slug/datacenter_cloud_infrastructure/vmware_vsphere/7_0)

# Local Usage 
After cloneing the repo, you must update the relevant answerfile  yaml to point to your ova and iso file, plus change any IP addresses or credentials.<br/>
When running for the first time you must run `./fix_dvs_for_7.sh` to enable creation of VDS v7 objects.

```
export PARENT_VCENTER_USERNAME="administrator@vsphere.local"
export PARENT_VCENTER_PASSWORD="VMware1!"
export VCSA_DIR="/home/matt/minio/vmware-products"
export ESXI_DIR="/home/matt/minio/vmware-products"

# Deploy vCenter and host/s
ansible-playbook deploy.yml --extra-vars="@answerfile-minimal.yml"
```

# Docker Usage 
After cloneing the repo, you must update the relevant answerfile  yaml to point to your ova and iso file, plus change any IP addresses or credentials.<br/>

```
export PARENT_VCENTER_USERNAME="administrator@vsphere.local"
export PARENT_VCENTER_PASSWORD="VMware1!"

docker run \
    --rm \
    --env PARENT_VCENTER_USERNAME=${PARENT_VCENTER_USERNAME} \
    --env PARENT_VCENTER_PASSWORD=${PARENT_VCENTER_PASSWORD} \
    --env VCSA_DIR='/software' \
    --env ESXI_DIR='/software' \
    --env ANSIBLE_FORCE_COLOR='true' \
    --volume ${PWD}:/work \
    --volume ${SOFTWARE_DIR}:/software \
    laidbackware/vsphere-ansible \
    ansible-playbook /work/deploy.yml \
        --extra-vars '@/work/answerfile-minimal.yml'  \
         -vvv 
```

# Known issues/future plans
- The TKGS playbook is broken with vCenter  7.0U1 due to a bug with the vCenter not creating tag categories correctly.
- VMs are not currently deployed into a folder or resource pool on the parent vCenter.
- Only local datastores are used. In the future NFS support may be added.