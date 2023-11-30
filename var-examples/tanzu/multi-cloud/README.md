# Tanzu Multi-Cloud with Avi Load Balancer
This will deploy using the standard 2 network topology

## Tested Versions
- NSX ALB Controller 22.1.4
- Tanzu Kubernetes Grid 2.4.0

## Additional Dependencies
In addition to the base dependencies, you will need to download and store the NSX-ALB OVA file in your software directory:
- [Tanzu download page](https://my.vmware.com/en/group/vmware/downloads/info/slug/infrastructure_operations_management/vmware_tanzu_kubernetes_grid/1_x)

## Architecture Nested
Below is the layout of the opinionated deployment, which can be customized by editing the vars file.</br></br>

```mermaid
flowchart LR
  router_net("Routed\nNetwork")
  esxi_host["Physical\nESXi Host"]
  base_pg("Base\nPort Group")
  trunk_pg("Trunk\nPort Group")
  nested_host["Nested\nESXi Host"]
  vcenter["vCenter"]
  nsx_alb_cont["NSX-ALB\nControllers"]
  base_vss("VM network\nStandard Switch")
  trunk_vds("Trunk\nDistributed Switch")
  nsx_seg["NSX-ALB\nSE Group"]
  tkg_vms["TKG VMs"]

  router_net --- esxi_host
  esxi_host --- base_pg & trunk_pg
  base_pg -- ESXi MGMT\n&\nVM Network ---- nested_host
  trunk_pg -- "Trunked Node\n& VIP VLANs" --- nested_host
  base_pg --- vcenter & nsx_alb_cont
  nested_host --- base_vss & trunk_vds
  base_vss & trunk_vds --- nsx_seg
  trunk_vds --- tkg_vms
  
  linkStyle 2,4,8,10,11 stroke:#00f

  style router_net fill:#aaa
  style base_pg fill:#aaa
  style trunk_pg fill:#aaa
  style base_vss fill:#aaa
  style trunk_vds fill:#aaa
  style esxi_host fill:#0ff
  style nested_host fill:#0c0
  style vcenter fill:#0c0
  style nsx_alb_cont fill:#0c0
  style nsx_seg fill:#FBCEB1
  style tkg_vms fill:#FBCEB1
```

</br>

- A single vCenter will be added.
- 2 networks are required. 
  - The base network must be a standard port group, where VMs can attach. This will appear as `vm-network` in the nested cluster.
  - The workload network can be on a standard port group or a trunk port group, where the nested host will add a VLAN tag. This will appear as `workload-pg` in the nested cluster.
  - DHCP must be setup on the workload network.
- NSX_ALB Controllers and Service Engine management interfaces will be added to `vm-network` on the 2nd and 3rd IP after the starting address.

## Architecture Not Nested
Below is the layout of the opinionated deployment, which can be customized by editing the vars file.</br></br>

```mermaid
flowchart LR
  router_net("Routed\nNetwork")
  esxi_host["Physical\nESXi Host"]
  base_pg("Base\nPort Group")
  nsx_alb_cont["NSX-ALB\nControllers"]
  nsx_seg["NSX-ALB\nSE Group"]
  tkg_vms["TKG VMs"]

  router_net --- esxi_host
  esxi_host --- base_pg
  base_pg --- nsx_alb_cont & nsx_seg & tkg_vms
  

  style router_net fill:#aaa
  style base_pg fill:#aaa
  style esxi_host fill:#0ff
  style nsx_alb_cont fill:#0c0
  style nsx_seg fill:#FBCEB1
  style tkg_vms fill:#FBCEB1
```

</br>

- 1 network is required. 
  - The base network must be a standard/distributed port group, where VMs can attach.
  - DHCP must be setup on the workload network to use the default TKGM management cluster yaml, although it can be modified to use node IPAM
- NSX_ALB Controllers and Service Engine management interfaces will be added to `vm-network` on the 2nd and 3rd IP after the starting address.

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