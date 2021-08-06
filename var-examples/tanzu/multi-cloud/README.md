# Tanzu Kubernetes for vSphere with Distributed Switching
This will deploy using the standard 2 network topology

## Dependencies
In addition to the base dependencies, you will need to download and store the NSX-ALB OVA file in your software directory:
- [Tanzu download page](https://my.vmware.com/en/group/vmware/downloads/info/slug/infrastructure_operations_management/vmware_tanzu_kubernetes_grid/1_x)

## Tested Versions
- Avi Controller 20.1.3-9085
- Tanzu Kubernetes Grid 1.3.1

## Instructions
In addition to the base instructions you will need to export the NSX-ALB (Avi) default password, which can be found on the Controller Ova download page.
```
export AVI_DEFAULT_PASSWORD=#######
```
You can now use the run command from the base instructions pointing to your updated vars file.