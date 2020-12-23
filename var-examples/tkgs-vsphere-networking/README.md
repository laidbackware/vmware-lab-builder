# Tanzu Kubernetes for vSphere with Distributed Switching
This will deploy using the standard 2 network topology

## Routing
By default a router will be created to bridge the workload and management networks. To be able to access resources deployed, you will need to add a static route to the router uplink which is the next IP after `hosting_network.base.starting_addr` <br/>
If you want to provide your own routing, you can remove the `router` section under `tkgs` and then setup your own routing for the network defined in `tkgs_workload_cidr`.

## IP Assignment on opinionated deployment

vCenter = `hosting_network.base.starting_addr`<br/>
router uplink = `hosting_network.base.starting_addr + 1`<br/>
first ESXi host = `hosting_network.base.starting_addr + 8`<br/>

## TODO!
- Add more debug statements to show config ahead of each task
- Add output at the end to show IPs of all deployed objects
- Add support in role haproxy for 3 network topology
- Add checks for common errors
- Add functionality to check and apply updates
