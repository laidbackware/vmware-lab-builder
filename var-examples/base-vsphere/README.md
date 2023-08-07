# Base vSphere

# Tested Versions
- vSphere 7.0 U3 and 8.0 U1

## Architecture
Below is the layout of the opinionated deployment, which can be customized by editing the vars file.</br></br>
```mermaid
flowchart LR
  router_net("Routed\nNetwork")
  esxi_host["Physical\nESXi Host"]
  base_pg("Base\nPort Group")
  nested_host["Nested\nHost"]
  vcenter["vCenter"]
  base_vss("VM network\nStandard Switch")

  router_net ---esxi_host
  esxi_host ---base_pg
  base_pg -- ESXi MGMT\n&\nVM Network ---nested_host
  base_pg ---vcenter
  nested_host ---base_vss

  style router_net fill:#aaa
  style base_pg fill:#aaa
  style base_vss fill:#aaa
  style esxi_host fill:#0ff
  style nested_host fill:#0c0
  style vcenter fill:#0c0
```
- A single vCenter will be added.
- Within the nested host the `vm-network` port group can be use to attach VMs to the routed network that has been passed through.



