# Base vSphere

# Tested Versions
- vSphere 7.0 U3 and 8.0 U1

## Architecture
Below is the layout of the opinionated deployment, which can be customized by editing the vars file.</br></br>
```mermaid
flowchart TD
  router_net(Routed Network)
  esxi_host[Physical\nESXi Host]
  router_net ---esxi_host
  base_pg(Base Port Group)
  esxi_host ---base_pg
  nested_host[Nested Host]
  vcenter[vCenter]
  base_pg -- ESXi Management\n&\nVM Network ---nested_host
  base_pg ---vcenter
  base_vss(VM network\nStandard Switch)
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



