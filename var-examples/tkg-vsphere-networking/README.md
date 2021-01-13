# Tanzu Kubernetes for vSphere with Distributed Switching
This will deploy using the standard 2 network topology

# Dependencies
In additiont the base dependencies, the following files need to be downloaded and stored in the software directoty:
- [VMware HA Proxy OVA](https://github.com/haproxytech/vmware-haproxy/releases/tag/v0.1.8)
- [VyOS OVA](https://downloads.vyos.io/release/legacy/1.1.8/vyos-1.1.8-amd64.ova)

# Routing
By default a router will be created to bridge the workload and management networks. To be able to access resources deployed, you will need to add a static route to the router uplink which is the next IP after `hosting_network.base.starting_addr` <br/>
If you want to provide your own routing, you can remove the `router` section under `tkgs` and then setup your own routing for the network defined in `tkgs_workload_cidr`.

# IP Assignment on opinionated deployment

vCenter = `hosting_network.base.starting_addr`<br/>
router uplink = `hosting_network.base.starting_addr + 1`<br/>
first ESXi host = `hosting_network.base.starting_addr + 8`<br/>

# Troubleshooting
- During creation the API will return errors for an extended period. The module will accept up to 150 seconds of errors, if the playbook ends with an error, check the UI to see if the action is progressing.

# Roadmap
- Add multi host option
- Add more debug statements to show config ahead of each task
- Add output at the end to show IPs of all deployed objects
- Add support in role haproxy for 3 network topology
- Add checks for common errors
- Add functionality to check and apply updates
- Add ability to shrink to 2 supervisors
  https://www.virtuallyghetto.com/2020/04/deploying-a-minimal-vsphere-with-kubernetes-environment.html
