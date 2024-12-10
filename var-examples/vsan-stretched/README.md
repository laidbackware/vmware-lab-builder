# Base vSphere

# Tested Versions
- vSphere 8.0 U3

## Architecture
Below is the layout of the opinionated deployment, which can be customized by editing the vars file.</br></br>
```mermaid
flowchart LR
  router_net("Routed\nNetwork")
  esxi_host["Physical\nESXi Host"]
  base_pg("Base\nPort Group")
  nested_host_1["Nested\nESXi Host 1"]
  nested_host_2["Nested\nESXi Host 2"]
  vcenter["vCenter"]
  base_vss("VM network\nStandard Switch")
  vsan_vds("VSAN private network")

  router_net ---esxi_host
  esxi_host ---base_pg
  base_pg -- ESXi MGMT\n&\nVM Network ---nested_host_1
  base_pg -- ESXi MGMT\n&\nVM Network ---nested_host_2
  base_pg ---vcenter
  nested_host_1 ---base_vss
  nested_host_2 ---base_vss
  nested_host_1 ---vsan_vds
  nested_host_2 ---vsan_vds

  style router_net fill:#aaa
  style base_pg fill:#aaa
  style base_vss fill:#aaa
  style vsan_vds fill:#aaa
  style esxi_host fill:#0ff
  style nested_host_1 fill:#0c0
  style nested_host_2 fill:#0c0
  style vcenter fill:#0c0
```
- A single vCenter will be added.
- 2 hosts are added without shared storage
- Within the nested host the `vm-network` port group can be use to attach VMs to the routed network that has been passed through.
- An internal only VDS is added for VSAN traffic



