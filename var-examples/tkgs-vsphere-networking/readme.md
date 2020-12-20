# Network space
## Routed
5 IPs for the masters
1 IPs for the HA Proxy management
?? for the VIPs

## Workload/private
?? for nodes

# Tasks To Do
## Add content library
## Get CA from HA Proxy
export GOVC_USERNAME=administrator@vsphere.local GOVC_PASSWORD=VMware1! GOVC_URL=https://192.168.0.171 GOVC_INSECURE=true
govc vm.info -e --json Lab/vm/haproxy |jq .VirtualMachines[0].Config.ExtraConfig | sed -e '1,/guestinfo.dataplaneapi.cacert/d' |head -1 |cut -d " " -f6 | tr -d '"' |base64 --decode


## Write module which can create the cluster using the API

### Get ID of storage policy
### Get ID of cluster
### Get content library IDs
### Get network IDs

curl -X  GET 'https://192.168.0.171/api/vcenter/namespace-management/clusters/domain-c8' -H 'vmware-api-session-id: 01241d5b179dd3937fc38e6300b0b7fb'

{
    "image_storage": {
        "storage_policy": "e029c0a9-34a1-43d1-b094-ef343b2a2a06"
    },
    "api_servers": [
        "192.168.0.177"
    ],
    "api_server_management_endpoint": "192.168.0.175",
    "master_NTP_servers": [
        "0.uk.pool.ntp.org"
    ],
    "ephemeral_storage_policy": "e029c0a9-34a1-43d1-b094-ef343b2a2a06",
    "service_cidr": {
        "address": "10.96.0.0",
        "prefix": 24
    },
    "size_hint": "TINY",
    "worker_DNS": [
        "192.168.0.110"
    ],
    "master_DNS": [
        "192.168.0.110"
    ],
    "network_provider": "VSPHERE_NETWORK",
    "master_storage_policy": "e029c0a9-34a1-43d1-b094-ef343b2a2a06",
    "stat_summary": {
        "cpu_used": 0,
        "storage_capacity": 0,
        "memory_used": 0,
        "cpu_capacity": 0,
        "memory_capacity": 0,
        "storage_used": 0
    },
    "api_server_cluster_endpoint": "192.168.0.175",
    "master_management_network": {
        "mode": "STATICRANGE",
        "address_range": {
            "subnet_mask": "255.255.252.0",
            "starting_address": "192.168.0.175",
            "gateway": "192.168.0.1",
            "address_count": 5
        },
        "network": "network-12"
    },
    "load_balancers": [
        {
            "address_ranges": [
                {
                    "address": "192.168.2.1",
                    "count": 29
                }
            ],
            "provider": "HA_PROXY",
            "id": "haproxy",
            "ha_proxy_info": {
                "servers": [
                    {
                        "port": 5556,
                        "host": "192.168.0.173"
                    }
                ],
                "certificate_authority_chain": "-----BEGIN CERTIFICATE-----\nMIIDoTCCAomgAwIBAgIJAK3YlacBEGUbMA0GCSqGSIb3DQEBBQUAMG4xCzAJBgNV\nBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlQYWxvIEFsdG8x\nDzANBgNVBAoMBlZNd2FyZTENMAsGA1UECwwEQ0FQVjEWMBQGA1UEAwwNMTkyLjE2\nOC4wLjE3MzAeFw0yMDExMDYxNTM0NTJaFw0zMDExMDQxNTM0NTJaMG4xCzAJBgNV\nBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlQYWxvIEFsdG8x\nDzANBgNVBAoMBlZNd2FyZTENMAsGA1UECwwEQ0FQVjEWMBQGA1UEAwwNMTkyLjE2\nOC4wLjE3MzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAMHc0sCj+C9k\nJl/NFgJWX/9/M4PagPwPlObloFYEbSIwKWlCdvzteTBiE8EXWSSpwlLIa7SB22lr\n7T4J8Ya/u2dcThgdTNiuNZA9OH32NFRHRnaPVuWENt4BRjm6DMVdfOmjqxDCUYUW\nKqIG5nMwX+wnoPpBc66p0/TjIc90j4Po3P9+oxVppxpz2n2vuIKB92bHTrRKcPvx\nOkr3Gcyys4wVrSzt8JViCR087oey+cv3yjvlwwDebtwLIHqc+tQ4x9br2P316M1x\nhAk9TfJlg5su57IyKkmdwIhIiTfb9rAOzcj3MnKcb5m3nwxWu2Nhe5rhcj49jDzH\nVX+LdX2TMJ0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC\nAYYwHQYDVR0OBBYEFHjZbFuOWMGWsZPylULgRUboA8V9MA0GCSqGSIb3DQEBBQUA\nA4IBAQCWGA0HgB20BmvR4baf0gsscoLPdAJxagrRom6BTLCbgVGa9lnXZ2eHrGQJ\nY5r4a53PfkNqFoA8wwXPIDVCZlQ0/wdt3/r030YscsXQo22bDKBdEv/uG15WfLNM\nHXjQLHBttaEAN5+ZcoptMPiVD3FGNX46yGZD6MburwYB7uSDYXa0mYh0rqTlVsXi\n8JvpdN1HiiT4zeNzwMLxY2F3v9vNVDSHrGPHzP6G+nz7ICOcfFSkbW4esvNvqCKH\nHq7SjlFWIfZIJYIN1MLif9W/HrqKPxVp9AxzMTU7vz1ZUx3RtE6XZEULU9xPjlC9\nF5gd3QCgcivLkRe5lIezVEAYKlGl\n-----END CERTIFICATE-----",
                "username": "haproxy"
            }
        }
    ],
    "config_status": "ERROR",
    "tls_management_endpoint_certificate": "-----BEGIN CERTIFICATE-----\nMIICyDCCAbCgAwIBAgIBADANBgkqhkiG9w0BAQsFADAVMRMwEQYDVQQDEwprdWJl\ncm5ldGVzMB4XDTIwMTEwNjE2MTExNFoXDTMwMTEwNDE2MTExNFowFTETMBEGA1UE\nAxMKa3ViZXJuZXRlczCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAM3t\nB0Zdy5Yjj7kSHwOwsOk+Fv+VxRcjMhVoKlDFyknypg+/QEY/YOgzAxmGOzstXOhL\nfR2kG2dDTPAsZPziOczz11q1dwURAG4uKqftPEwc79l4meU98TKE5jfFQba9HJKH\n4w84BKgItVZdUIqqULGNDOQFCT4/29/DkYWwJzEiUnb8loE/GxqNP208ZTwyrcj3\ncJsoMTZoW7RnAQPVrVr102ysIMhKtmW9VJbhmo89ga+Gg+aE6c4hb69As0hS/nOM\nLIwFO3BOl6ROmvxN/+q7XAE3TCndNZxoerQPJToneCRkSk7OBNi0jJV/Bd0dAhPQ\nJscJlMBLAIFj9F51qvUCAwEAAaMjMCEwDgYDVR0PAQH/BAQDAgKkMA8GA1UdEwEB\n/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBACNKQ244SVbWr9T8SAytYsHnaHXL\nC/XXI0t0dcipO02e/Jbv9c3b2dBngFjvR1Oe8L9LnjeMrhKjQmQuIuN6aVwS2+yq\nQe0e880bKcH8oUIcY1Dh/ed6DAJMZ7/nwcf06s7D53L2Quar05oF4Oj4+5V4S8m9\nsZmEdxhMCKGsczliwaUm420L0Hu5iZqX2os/FEH2/4mM9t93F2+gdz8+y5dqkliO\n+4L2TZr5Pes8LGQJ82lRLO71sWW7RDklvKqq7YdR6Eq4SYstUiO3lYUMX5q0RSAB\nnuokzqe+RyuioeMddexQGrSDYTHU/5iU/2+qBjVXBBJG6sDsuF3H7RSWeWA=\n-----END CERTIFICATE-----\n",
    "kubernetes_status": "ERROR",
    "kubernetes_status_messages": [
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "Kubelet stopped posting node status."
                ],
                "default_message": "Node is not healthy and is not accepting pods. Details Kubelet stopped posting node status..",
                "localized": "Node is not healthy and is not accepting pods. Details Kubelet stopped posting node status..",
                "id": "vcenter.wcp.node.kubenotready"
            }
        },
        {
            "severity": "WARNING",
            "details": {
                "args": [
                    "192.168.0.175",
                    "Get https://192.168.0.175:6443/healthz?timeout=5s: dial tcp 192.168.0.175:6443: connect: no route to host"
                ],
                "default_message": "Kubernetes cluster health endpoint problem at 192.168.0.175. Details: Get https://192.168.0.175:6443/healthz?timeout=5s: dial tcp 192.168.0.175:6443: connect: no route to host",
                "localized": "Kubernetes cluster health endpoint problem at 192.168.0.175. Details: Get https://192.168.0.175:6443/healthz?timeout=5s: dial tcp 192.168.0.175:6443: connect: no route to host",
                "id": "vcenter.wcp.cluster.k8s.health.endpoint.problem"
            }
        },
        {
            "severity": "WARNING",
            "details": {
                "args": [
                    "vmware-system-netop/vmware-system-netop-controller-manager"
                ],
                "default_message": "Infrastructure Deployment identifier {1} is not fully available. This may affect your cluster networking.",
                "localized": "Infrastructure Deployment identifier {1} is not fully available. This may affect your cluster networking.",
                "id": "vcenter.wcp.netoperator.deployment.unavailable"
            }
        }
    ],
    "tls_endpoint_certificate": "",
    "messages": [
        {
            "severity": "WARNING",
            "details": {
                "args": [
                    "WARNING"
                ],
                "default_message": "Error configuring cluster NIC on master VM. This operation is part of API server configuration and will be retried.",
                "id": "vcenter.wcp.cluster.nic.config.error"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "42156ffdcb9a186486ce8f8b7fe15cf1",
                    "Script ['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '42156ffdcb9a186486ce8f8b7fe15cf1', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\''] failed: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '42156ffdcb9a186486ce8f8b7fe15cf1', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\'']' returned non-zero exit status 1."
                ],
                "default_message": "System error occurred on control plane 42156ffdcb9a186486ce8f8b7fe15cf1. Details Script ['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '42156ffdcb9a186486ce8f8b7fe15cf1', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\''] failed: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '42156ffdcb9a186486ce8f8b7fe15cf1', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\'']' returned non-zero exit status 1.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "42156ffdcb9a186486ce8f8b7fe15cf1",
                    "Failed to handle domain change. Err Command '['kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'apply', '-f', '/usr/lib/vmware-wcp/objects/common/00-wcp/wcp-wcpsvc-cluster-admin-role-binding.yaml']' returned non-zero exit status 1."
                ],
                "default_message": "System error occurred on control plane node 42156ffdcb9a186486ce8f8b7fe15cf1. Details Failed to handle domain change. Err Command '['kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'apply', '-f', '/usr/lib/vmware-wcp/objects/common/00-wcp/wcp-wcpsvc-cluster-admin-role-binding.yaml']' returned non-zero exit status 1.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "42156ffdcb9a186486ce8f8b7fe15cf1",
                    "Failed to sync changes: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', '-n', 'kube-system', 'get', 'networkinterfaces', '-o', 'json']' returned non-zero exit status 1.. Will be retried."
                ],
                "default_message": "System error occurred on control plane node 42156ffdcb9a186486ce8f8b7fe15cf1. Details Failed to sync changes: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', '-n', 'kube-system', 'get', 'networkinterfaces', '-o', 'json']' returned non-zero exit status 1.. Will be retried.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "4215a2e396b597a5352a0b837e24c19c",
                    "Script ['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '4215a2e396b597a5352a0b837e24c19c', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\''] failed: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '4215a2e396b597a5352a0b837e24c19c', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\'']' returned non-zero exit status 1."
                ],
                "default_message": "System error occurred on control plane 4215a2e396b597a5352a0b837e24c19c. Details Script ['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '4215a2e396b597a5352a0b837e24c19c', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\''] failed: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '4215a2e396b597a5352a0b837e24c19c', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\'']' returned non-zero exit status 1.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "4215a2e396b597a5352a0b837e24c19c",
                    "Failed to handle domain change. Err Command '['kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'apply', '-f', '/usr/lib/vmware-wcp/objects/common/00-wcp/wcp-wcpsvc-cluster-admin-role-binding.yaml']' returned non-zero exit status 1."
                ],
                "default_message": "System error occurred on control plane node 4215a2e396b597a5352a0b837e24c19c. Details Failed to handle domain change. Err Command '['kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'apply', '-f', '/usr/lib/vmware-wcp/objects/common/00-wcp/wcp-wcpsvc-cluster-admin-role-binding.yaml']' returned non-zero exit status 1.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "4215a2e396b597a5352a0b837e24c19c",
                    "Failed to sync changes: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', '-n', 'kube-system', 'get', 'networkinterfaces', '-o', 'json']' returned non-zero exit status 1.. Will be retried."
                ],
                "default_message": "System error occurred on control plane node 4215a2e396b597a5352a0b837e24c19c. Details Failed to sync changes: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', '-n', 'kube-system', 'get', 'networkinterfaces', '-o', 'json']' returned non-zero exit status 1.. Will be retried.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "4215b4572ec28ec051a6fe96772e2499",
                    "Script ['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '4215b4572ec28ec051a6fe96772e2499', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\''] failed: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '4215b4572ec28ec051a6fe96772e2499', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\'']' returned non-zero exit status 1."
                ],
                "default_message": "System error occurred on control plane 4215b4572ec28ec051a6fe96772e2499. Details Script ['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '4215b4572ec28ec051a6fe96772e2499', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\''] failed: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'get', 'node', '4215b4572ec28ec051a6fe96772e2499', '-o', 'jsonpath=\\'{.status.addresses[?(@.type == \"InternalIP\")].address}\\'']' returned non-zero exit status 1.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "4215b4572ec28ec051a6fe96772e2499",
                    "Failed to handle domain change. Err Command '['kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'apply', '-f', '/usr/lib/vmware-wcp/objects/common/00-wcp/wcp-wcpsvc-cluster-admin-role-binding.yaml']' returned non-zero exit status 1."
                ],
                "default_message": "System error occurred on control plane node 4215b4572ec28ec051a6fe96772e2499. Details Failed to handle domain change. Err Command '['kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', 'apply', '-f', '/usr/lib/vmware-wcp/objects/common/00-wcp/wcp-wcpsvc-cluster-admin-role-binding.yaml']' returned non-zero exit status 1.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        },
        {
            "severity": "ERROR",
            "details": {
                "args": [
                    "4215b4572ec28ec051a6fe96772e2499",
                    "Failed to sync changes: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', '-n', 'kube-system', 'get', 'networkinterfaces', '-o', 'json']' returned non-zero exit status 1.. Will be retried."
                ],
                "default_message": "System error occurred on control plane node 4215b4572ec28ec051a6fe96772e2499. Details Failed to sync changes: Command '['/usr/bin/kubectl', '--kubeconfig', '/etc/kubernetes/admin.conf', '-n', 'kube-system', 'get', 'networkinterfaces', '-o', 'json']' returned non-zero exit status 1.. Will be retried.",
                "id": "vcenter.wcp.master.guest.systemerror"
            }
        }
    ],
    "default_kubernetes_service_content_library": "fe37da67-10e2-43eb-a9aa-7305a394114a",
    "workload_networks": {
        "supervisor_primary_workload_network": {
            "vsphere_network": {
                "portgroup": "dvportgroup-19",
                "address_ranges": [
                    {
                        "address": "192.168.2.16",
                        "count": 14
                    }
                ],
                "subnet_mask": "255.255.252.0",
                "gateway": "192.168.0.1"
            },
            "network_provider": "VSPHERE_NETWORK",
            "network": "network-1"
        }
    }
}