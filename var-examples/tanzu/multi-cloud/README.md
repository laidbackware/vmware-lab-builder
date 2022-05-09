# Tanzu Multi-Cloud with Avi Load Balancer
This will deploy using the standard 2 network topology

## Tested Versions
- Avi Controller 20.1.6
- Tanzu Kubernetes Grid 1.5.1

## Additional Dependencies
In addition to the base dependencies, you will need to download and store the NSX-ALB OVA file in your software directory:
- [Tanzu download page](https://my.vmware.com/en/group/vmware/downloads/info/slug/infrastructure_operations_management/vmware_tanzu_kubernetes_grid/1_x)

## Architecture
Below is the layout of the opinionated deployment, which can be customized by editing the vars file.</br></br>
![Architecture Diagram](architecture-tanzu-mulit-cloud-avi.png)
- A single vCenter will be added.
- Within the nested host the `vm-network` port group can be use to attach VMs to the routed network that has been passed through.
- A Trunk interface passes through 2 VLANs from the routed network to the VDS on vmnic1 on the nested ESXi host.
  - 1 VLAN hosts Avi VIPs
  - 1 VLAN hosts the TKG nodes
  - DHCP must be setup on the TKG nodes network
- Avi SE management interfaces will be added to `vm-network` on the 2nd and 3rd IP after the starting address.

## Instructions
In addition to the base instructions you will need to export the NSX-ALB (Avi) default password, which can be found on the Controller Ova download page.
```
export AVI_DEFAULT_PASSWORD=#######
```
You can now use the run command from the base instructions pointing to your updated vars file.

## IP Assignment on opinionated deployment

vCenter = `hosting_network.base.starting_addr`<br/>
Avi Controller = `hosting_network.base.starting_addr + 1`<br/>
First ESXi host = `hosting_network.base.starting_addr + 4`<br/>

## Known Issues
- Creation of the first VLAN segments can take some time whilst the Transport Zones are configured.
- A number of Ansible for NSX-T modules are not properly idempotent and report changed even though no change has been made.