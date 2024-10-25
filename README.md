# vmware-lab-builder

Build a nested vSphere lab with Ansible.

## <span style="color:red">Breaking Changes</span>

A change in ansible-for-nsxt requires that the options for field `transport_type` change from `OVERLAY` and `VLAN` to `OVERLAY_BACKED` and `VLAN_BACKED`.

Support for NSX 3.0 has been dropped. See `nsx-3.0-support` branch for legacy support.

## <span style="color:red">Warnings</span>

When pulling this repo, be sure to use the latest version of the container image or check the dependency setup, to ensure the the roles have all the required dependencies.

Python 3.12 is currently not supported on mainline`ansible-for-nsxt`, due to a bug using a removed funciton. [Bug](https://github.com/vmware/ansible-for-nsxt/issues/517). Recommend using the fixed [fork linked in this repo](#local-usage) or v11 of the Docker image.

`ansible-core` => 2.17.1 is not supported with `ansible-for-nsxt`, recommend using 2.16.x until it is fixed. See [this PR](https://github.com/vmware/ansible-for-nsxt/pull/509) and commit if this affects you..

## Description

You can use the ansible playbooks in this repo to build out nested ESXi hosts, deploy a vCenter and configure clusters. ESXi/vCenter 7.0 and 8.0 are supported. The main design goal of this project is to be able to provide both opinionated deployment with few variables and to have the ability to fully customize the deployment.

## Dependencies

Infrastructure:
- A machine which is able to run docker that also has access to where the VMs will be deployed.
- A licensed vSphere cluster.
- A datastore to host VMs of at least 200GB.
- An NTP server which is reachable by IP.
- All port groups assigned to nested ESXi VMs should have [Mac Learning](https://www.virtuallyghetto.com/2018/04/native-mac-learning-in-vsphere-6-7-removes-the-need-for-promiscuous-mode-for-nested-esxi.html) or promiscuous mode enabled on the parent port group. Mac learning is preferred. If your physical host is vSphere 8.0, you also need to enable Forget Transmits.
  
- Software downloads should be placed in a single directory:
- [ESXi OVA images](https://williamlam.com/nested-virtualization/nested-esxi-virtual-appliance)
- [vCenter ISO](https://my.vmware.com/en/group/vmware/downloads/info/slug/datacenter_cloud_infrastructure/vmware_vsphere/7_0) - For command line downloading see [vmd](https://github.com/laidbackware/vmd)

## Status and Versions

This release has been tested with the following components and should be backwards compatible.</br>
| vCenter Version | ESXi Version |
| --------------- | ------------ |
| 7.0U3           | 7.0U3        |
| 8.0U3           | 8.0U3        |

The pattern names below match the sub-directory under `var-examples` where examples can be found.</br>

| Pattern Name              | Product Versions                     | Status |
| ------------------------- | ------------------------------------ | ------ |
| base-vsphere              | n/a                                  | Stable |
| nsxt                      | NSX-T 3.2,4.x                        | Stable |
| tanzu/multi-cloud         | NSX-ALB 20.1.7                       | Stable |
| tanzu/vsphere-nsxt        | NSX-T 3.1, 3.2, 4.0                  | Stable |
| tanzu/vsphere-vds-alb     | NSX-ALB 20.1.7                       | Stable |
| tanzu/vsphere-vds-haproxy | haproxy                              | Stable |
| tanzu/integrated          | TKGi 1.13-1.16 & NSX-T 3.x, 4.0      | Stable |
| tanzu/application-service | TAS 2.11, 2.13, 4.0 & NSX-T 3.2, 4.1 | Stable |

## Usage with Docker

Each deployment pattern has an opinionated and some have a custom example(which may be out of date). The idea of the opinionated deployment is that the user has to provide the minimum of configuration and the remainder of the options are calculated for them. Whereas the custom example has to have all sections built up by hand. Either of the examples types can be fully customized.<br/>

You must export the credentials to you existing vCenter as environmental variables along with the path on your local machine which contains the software listed above.</br>
```
export PARENT_VCENTER_USERNAME="administrator@vsphere.local"
export PARENT_VCENTER_PASSWORD="VMware1!"
export SOFTWARE_DIR="$HOME/Downloads/vmware-products" 
```
It is recommended to use [direnv](https://direnv.net/) and have the above export commands in a .envrc file.<br/>

### Known Issues

Docker Desktop on Mac has known network performance issues resulting in very slow OVA upload speeds. It's recommended to use docker-ce natively from a Linux machine/VM or to run the playbooks locally - see [Local Usage](#local-usage).

### Deploying

After cloning this repo, you should copy and update the relevant vars yaml from the var-examples directory, making sure to include your ova and iso file names, and to change any IP addresses and credentials.<br/>

Check the readme file in the example directory for any additional steps which may be needed for that pattern.<br/>

The example below will deploy a single host and a vCenter, plus create a cluster with the minimum feature set. It should be run from the root of this repo and will map the repo directories under `/work` within the container.<br/>
```
# This setups up the alias, which handles environment variables and volumes
alias lab-builder="docker run --rm \
    --env PARENT_VCENTER_USERNAME=${PARENT_VCENTER_USERNAME} \
    --env PARENT_VCENTER_PASSWORD=${PARENT_VCENTER_PASSWORD} \
    --env SOFTWARE_DIR='/software_dir' \
    --env ANSIBLE_FORCE_COLOR='true' \
    --env NSXT_LICENSE_KEY=${NSXT_LICENSE_KEY:-na} \
    --env AVI_DEFAULT_PASSWORD=\"${AVI_DEFAULT_PASSWORD:-na}\" \
    --volume ${SOFTWARE_DIR}:/software_dir \
    --volume ${PWD}:/work \
    laidbackware/vmware-lab-builder:v10 \
    ansible-playbook"

# This command is run inside the container, so point to the `/work` directory within the container.
lab-builder /work/deploy.yml --extra-vars '@/work/var-examples/base-vsphere/minimal-opinionated.yml'
```

### Destroying

To delete the nested lab use destroy.yml, which will delete all VMs from the parent vCenter.</br/>
This requires the `lab-builder` alias is set from the [Deploying](#deploying) 
```
lab-builder /work/destroy.yml \
    --extra-vars '@/work/var-examples/base-vsphere/minimal-opinionated.yml'
```

## Troubleshooting

The vCenter install can take a long time. You can check the progress by browsing to https://<vcenter IP>:5480. If the vCenter install fails, check the `vcsa-cli-installer.log` file which can be found in a created directory under /tmp.<br/>

To debug in docker, first enter the container with bash, then run the playbook. This way the vCenter build logs will be available after the failure.
```
# This command will start a bash shell within the container
docker run  -it --rm \
    --env PARENT_VCENTER_USERNAME=${PARENT_VCENTER_USERNAME} \
    --env PARENT_VCENTER_PASSWORD=${PARENT_VCENTER_PASSWORD} \
    --env SOFTWARE_DIR='/software_dir' \
    --env ANSIBLE_FORCE_COLOR='true' \
    --env NSXT_LICENSE_KEY=${NSXT_LICENSE_KEY:-na} \
    --env AVI_DEFAULT_PASSWORD=${AVI_DEFAULT_PASSWORD:-na} \
    --volume ${SOFTWARE_DIR}:/software_dir \
    --volume ${PWD}:/work \
    laidbackware/vmware-lab-builder:v10 \
    /bin/bash

# Then the playbook can be triggered
ansible-playbook /work/deploy.yml --extra-vars '@/work/<path>/<file>.yml'
```
If adding new variables to the vars file be sure to only use underscores as variable names and not hyphens.

## Roadmap

For solution specific features, check the relevant example directory.
- Switch all OVAs to be uploaded and used from a Content library, to speed up deployment
- Support for NSX-ALB 21.1
- Add ability to create TKGS namespaces
- Add ability to create guest clusters for TKGS
- Add ability to deploy VMs to folders and resource pools on parent vCenter
- Add support for VSAN configuration

## Docker Image Build

`qemu` and `docker buildx` are used to build the images to give portability.

From the root of the repo. Note no-cache flag used to force builds to pickup any changes to the git repos.

One time build setup process on debian systems:

```sh
sudo apt-get install qemu binfmt-support qemu-user-static
docker buildx create --name multi-arch --driver docker-container --platform linux/amd64,linux/arm64
```

Build command:

```
docker buildx build --push --platform linux/arm64,linux/amd64 --tag laidbackware/vmware-lab-builder:v10 ./docker
```

## Local Usage

Software dependencies for Linux:
- Ansible 2.13 or higher.
- Linux tools `apt-get install libarchive-tools sshpass python3-pip git python3-jmespath sshpass`
- Install all necessary Python modules
    ```
    pip install -r requirements.txt
    ```
- Add necessary Ansible collections. Force switch will ensure it is upgraded.
   ```
   ansible-galaxy collection install community.vmware:4.5.0 --force
   ansible-galaxy collection install vmware.alb:22.1.4 --force
   ansible-galaxy collection install git+https://github.com/laidbackware/ansible-for-nsxt.git,upstream-fixes --force
   ansible-galaxy collection install git+https://github.com/laidbackware/ansible-for-vsphere-tanzu.git,ansible-galaxy --force
   ```
