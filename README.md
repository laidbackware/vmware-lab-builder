# vsphere-ansible-lab-builder
Build a nested vSphere lab with Ansible

## Description
You can use the ansible playbooks in this repo to build out nested ESXi hosts, deploy a vCenter and configure clusters. ESXi/vCenter 6.7 and 7.0 are supported.

# Dependencies
The following procedure has been developed on a debian based linux machine.<br/>
Versions:
- Ansible 2.10 or higher
- Linux tools `apt-get install xorriso sshpass python-pip git`
- Python modules `pip3 install pyvmomi`
- Install [vSphere Automation SDK](https://github.com/vmware/vsphere-automation-sdk-python)
    `pip install --upgrade pip setuptools`
    `pip install --upgrade git+https://github.com/vmware/vsphere-automation-sdk-python.git`
- [ESXi OVA images](https://www.virtuallyghetto.com/nested-virtualization/nested-esxi-virtual-appliance)
- [vCenter ISO](https://my.vmware.com/en/group/vmware/downloads/info/slug/datacenter_cloud_infrastructure/vmware_vsphere/7_0)

# Usage
After cloneing the repo, you must update the relevant answerfile  yaml to point to your ova and iso file, plus change any IP addresses or credentials.<br/>
When running for the first time you must run `./fix_dvs_for_7.sh` to enable creation of VDS v7 objects.

```
export PARENT_VCENTER_USERNAME="administrator@vsphere.local"
export PARENT_VCENTER_PASSWORD="VMware1!"
TMPDIR=$(mktemp -d) || exit 1
echo "Temp dir is ${TMPDIR}"

# Deploy vCenter and host/s
ansible-playbook deploy.yml --extra-vars="@answerfile-minimal.yml"  --extra-vars "tmp_dir=${TMPDIR}"
```

## with Docker

### Building the vsphere-ansible Docker image

```
docker build --tag vsphere-ansible .
```

### Build vSphere lab

```
docker run \
    --rm \
    --env PARENT_VCENTER_USERNAME='administrator@vsphere.local' \
    --env PARENT_VCENTER_PASSWORD='VMware1!' \
    --volume ${PWD}:/work \
    vsphere-ansible \
    ansible-playbook deploy.yml \
        --extra-vars '@answerfile-minimal.yml'  \
        --extra-vars 'tmp_dir=/tmp'
```

# Known issues/future plans
- The TKGS playbook is broken with vCenter  7.0U1 due to a bug with the vCenter not creating tag categories correctly.
- VMs are not currently deployed into a folder or resource pool
- Only local datastores are used. In the future NFS support may be added.