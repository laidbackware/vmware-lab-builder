#!/usr/bin/python
# -*- coding: utf-8 -*-
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: vmware_namespace_cluster_vds_manager
short_description: Enable, disable and update namespaces on a vSphere cluster
description:
- TODO
author:
- Matt Proud (@laidbackware)
notes:
- Tested on vSphere 7.0u1
requirements:
- python >= 3.5
- PyVmomi
- vSphere Automation SDK
options:
    
extends_documentation_fragment:
- community.vmware.vmware_rest_client.documentation

'''
EXAMPLES = r'''
- name: Enable Namespaces on Cluster
  community.vmware.vmware_namespace_cluster_vds_manager:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    content_library_name: "tkgs-library"
    cluster_name: tkgs-cluster
    dns_search_domains: ["home.local"]
    dns_servers: ["192.168.0.110"]
    haproxy_ca_chain: |
        -----BEGIN CERTIFICATE-----
        MIIDoTCCAomgAwIBAgIJAME387BtGGikMA0GCSqGSIb3DQEBBQUAMG4xCzAJBgNV
        BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlQYWxvIEFsdG8x
        DzANBgNVBAoMBlZNd2FyZTENMAsGA1UECwwEQ0FQVjEWMBQGA1UEAwwNMTkyLjE2
        OC4wLjE3MzAeFw0yMDEyMTgxMzI0NDhaFw0zMDEyMTYxMzI0NDhaMG4xCzAJBgNV
        BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlQYWxvIEFsdG8x
        DzANBgNVBAoMBlZNd2FyZTENMAsGA1UECwwEQ0FQVjEWMBQGA1UEAwwNMTkyLjE2
        OC4wLjE3MzCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBAOpaFdTntwKj
        7iEThLB7+GA4SIxJLHXmnh05Y2L0lZ0TMz2h2tsnI+Hv2x9QlVQtIiSpTxb89xl8
        3qE/IBvaNc/8vRY8h4gaFbkh0GS+9JoQzPFYnZrI9fzNwh2cyKqigzzJEe61JX0p
        XhN42lzdziUu2qYgAvwLPne3UCKI/CenU0WHOcq61cCEaE07nPKbjKgLD20SSiv/
        f+4JnvzeAU7d6De+78mQIxTCyBeQG9ZeE/y22fHoNbIu5rQKIfhYtyDuv8mpC3Z3
        HyRKL4z/DcO0aLanbYQsFB0IhI1ZZvkqcRIarI0atPJPjxcl7xHtcojTTfpy0QvH
        K77D81ZEQB8CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
        AYYwHQYDVR0OBBYEFC+EVdoW1yy6sv1S58G6imTwXRGbMA0GCSqGSIb3DQEBBQUA
        A4IBAQBn9U5aJSOmLRzmHWxgxfnu+28ksOCsuVpBVHm6+q7mrA/ArbuMncUBbnO1
        lCxDTJq+LOjAtDJeMhIDEPnCRBeBcrsvvoRIV2YR1kvrhCaWZoNTT07Jm9K5wBYx
        BTbJdvnp7kI0e/sgpRlRGFO/31ey5ItknQXGCTJ4qzp3KbtQ5qz+dvGz0iFykj31
        DYTqg5Da9WYBTnCm2a641OuoVfkK9Toq5kISTNkoi8JLhlJwQUuRFRE6OJfiLCQs
        0pC0Q8G1u2ToTZE0jntjy4BzxGZq26A/SrpFP/d8dksjo1IpRNLvA26+BJ7Ir/qY
        r32oIPyK4InlL/FMoVrmefDRTAwy
        -----END CERTIFICATE-----
    haproxy_management_ip: "192.168.0.173"
    haproxy_password: haproxy
    haproxy_username: password_here
    management_port_group: routed-pg
    management_gateway: "192.168.0.1"
    management_starting_address: "192.168.0.174"
    management_netmask: "255.255.252.0"
    ntp_servers: ["192.168.0.1"]
    workload_gateway: "172.31.0.1"
    workload_portgroup: private-pg
    workload_range_starting_ip: "172.31.0.3"
    workload_range_count: 40
    workload_netmask: "255.255.255.0"
    services_cidr: "10.255.255.0"
    supervisor_size: tiny
    storage_policy_name: "tkgs-storage-policy"
    state: present
  delegate_to: localhost
  async: 1800
  poll: 5

- name: Disable Namespaces on Cluster
  community.vmware.vmware_namespace_cluster_vds_manager:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    cluster_name: tkgs-cluster
    state: absent
  delegate_to: localhost
'''

RETURN = r'''
namespace_cluster_vds_info:

'''

import uuid
from time import sleep
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.vmware.plugins.module_utils.vmware_rest_client import VmwareRestClient
from ansible_collections.community.vmware.plugins.module_utils.vmware import PyVmomi
import urllib3
urllib3.disable_warnings()

HAS_VAUTOMATION_PYTHON_SDK = False
try:
    from com.vmware.vcenter.namespace_management_client import Clusters, LoadBalancers, Ipv4Cidr, Networks, IPRange
    HAS_VAUTOMATION_PYTHON_SDK = True
except ImportError:
    pass


class VmwareNamespaceClusterVdsManage(VmwareRestClient):
    def __init__(self, module):
        """Constructor."""
        super(VmwareNamespaceClusterVdsManage, self).__init__(module)

        self.cluster_object = Clusters(self.api_client._stub_config)
        self.loadbalancer_object = LoadBalancers(self.api_client._stub_config)
        self.network_object = Networks(self.api_client._stub_config)

        self.cluster_name = self.get_cluster_by_name(self.params.get('cluster_name'))
        self.content_library_name = self.params.get('content_library_name')
        self.dns_search_domains = self.params.get('dns_search_domains')
        self.dns_servers = self.params.get('dns_servers')
        self.haproxy_ca_chain = self.params.get('haproxy_ca_chain')
        self.haproxy_management_ip = self.params.get('haproxy_management_ip')
        self.haproxy_password = self.params.get('haproxy_password')
        self.haproxy_username = self.params.get('haproxy_username')
        self.haproxy_range_start_address = self.params.get('haproxy_range_start_address')
        self.haproxy_range_count = self.params.get('haproxy_range_count')
        self.management_port_group = self.params.get('management_port_group')
        self.management_gateway = self.params.get('management_gateway')
        self.management_starting_address = self.params.get('management_starting_address')
        self.management_netmask = self.params.get('management_netmask')
        self.ntp_servers = self.params.get('ntp_servers')
        self.workload_gateway = self.params.get('workload_gateway')
        self.workload_portgroup = self.params.get('workload_portgroup')
        self.workload_range_starting_ip = self.params.get('workload_range_starting_ip')
        self.workload_range_count = self.params.get('workload_range_count')
        self.workload_netmask = self.params.get('workload_netmask')
        self.services_cidr = self.params.get('services_cidr')
        self.supervisor_size = self.params.get('supervisor_size')
        self.storage_policy_name = self.params.get('storage_policy_name')

    def process_state(self):
        """
        Manage states of Content Library
        """
        self.desired_state = self.params.get('state')
        namespace_cluster_states = {
            'absent': {
                'present': self.state_disable_cluster,
                'absent': self.state_exit_unchanged,
            },
            'present': {
                'present': self.state_update_cluster,
                'absent': self.state_enable_cluster,
            }
        }
        namespace_cluster_states[self.desired_state][self.check_namespace_cluster_status(self.desired_state)]()

    def check_namespace_cluster_status(self, desired_state):
        """
        Check if Content Library exists or not
        Returns: 'present' if library found, else 'absent'

        """
        try:
            existing_cluster_status = self.cluster_object.get(self.cluster_name).config_status
            if existing_cluster_status == "RUNNING" or existing_cluster_status == "ERROR":
                return 'present'
            elif existing_cluster_status == "CONFIGURING" and desired_state == "absent":
                return 'present'
            else:
                self.module.fail_json(msg="Operation cannot continue. Cluster [%s] is currently in state %s" % (self.cluster_name, existing_cluster_status))
        except Exception:
            return 'absent'
        # ret = 'present' if self.library_name in self.local_libraries else 'absent'
        # return ret
        

    def state_exit_unchanged(self):
        """
        Return unchanged state

        """
        self.module.exit_json(changed=False)

    def get_cluster_by_name(self, cluster_name):
        vsphere_clusters = self.api_client.vcenter.Cluster.list()
        for cluster in vsphere_clusters:
            if cluster.name == cluster_name:
                return cluster.cluster
        raise Exception("Cluster not found")

    def state_enable_cluster(self):
        """
        Enable workload management on a cluster using vSphere networking.
        """
        def get_network_by_name(network_name):
            vsphere_networks = self.api_client.vcenter.Network.list()
            for network in vsphere_networks:
                if network.name == network_name:
                    return network.network
            raise Exception("Network not found")

        def get_storage_policy_by_name(storage_policy_name):
            vsphere_storage_policys = self.api_client.vcenter.storage.Policies.list()
            for storage_policy in vsphere_storage_policys:
                if storage_policy.name == storage_policy_name:
                    return storage_policy.policy
            raise Exception("storage_policy not found")

        tkgs_storage_policy_identifier = get_storage_policy_by_name(self.storage_policy_name)

        management_network_range = self.cluster_object.Ipv4Range()
        management_network_range.starting_address = self.management_starting_address
        management_network_range.address_count = 5
        management_network_range.subnet_mask = self.management_netmask
        management_network_range.gateway = self.management_gateway

        management_network_spec = self.cluster_object.NetworkSpec()
        management_network_spec.network = get_network_by_name(self.management_port_group)
        management_network_spec.mode = "STATICRANGE"
        management_network_spec.address_range = management_network_range

        #TODO check HA proxy connection and error if issues
        haproxy_spec = self.loadbalancer_object.HAProxyConfigCreateSpec()
        haproxy_spec.servers = [self.loadbalancer_object.Server(host=self.haproxy_management_ip ,port=5556)]
        haproxy_spec.username = self.haproxy_username
        haproxy_spec.password = self.haproxy_password
        haproxy_spec.certificate_authority_chain = self.haproxy_ca_chain

        loadbalancer_spec = self.loadbalancer_object.ConfigSpec()
        loadbalancer_spec.id = "haproxy"
        loadbalancer_spec.address_ranges = [IPRange(address=self.haproxy_range_start_address, count=int(self.haproxy_range_count))]
        loadbalancer_spec.provider = "HA_PROXY"
        loadbalancer_spec.ha_proxy_config_create_spec = haproxy_spec

        #TODO fail if not legal CIDR
        services_cidr_split = self.services_cidr.split('/')
        services_cidr = Ipv4Cidr(address=services_cidr_split[0], prefix=int(services_cidr_split[1]))

        workload_vsphere_network_spec = self.network_object.VsphereDVPGNetworkCreateSpec()
        workload_vsphere_network_spec.portgroup = get_network_by_name(self.workload_portgroup)
        workload_vsphere_network_spec.address_ranges = [IPRange(address=self.workload_range_starting_ip, 
                                                                count=self.workload_range_count)]
        workload_vsphere_network_spec.gateway = self.workload_gateway
        workload_vsphere_network_spec.subnet_mask = self.workload_netmask

        workload_network_spec = self.network_object.CreateSpec()
        workload_network_spec.network = "network-1"
        workload_network_spec.network_provider = self.cluster_object.NetworkProvider.VSPHERE_NETWORK
        workload_network_spec.vsphere_network = workload_vsphere_network_spec

        workload_network_enable_spec = self.cluster_object.WorkloadNetworksEnableSpec()
        workload_network_enable_spec.supervisor_primary_workload_network = workload_network_spec

        cluster_spec = self.cluster_object.EnableSpec()
        cluster_spec.size_hint = self.supervisor_size
        cluster_spec.service_cidr = services_cidr
        cluster_spec.network_provider = "VSPHERE_NETWORK"
        cluster_spec.workload_networks_spec = workload_network_enable_spec
        cluster_spec.workload_ntp_servers = self.ntp_servers
        cluster_spec.load_balancer_config_spec = loadbalancer_spec
        cluster_spec.master_management_network = management_network_spec
        cluster_spec.master_dns = self.dns_servers
        cluster_spec.worker_dns = self.dns_servers
        cluster_spec.master_dns_search_domains = self.dns_search_domains
        cluster_spec.master_ntp_servers = self.ntp_servers
        cluster_spec.master_storage_policy = tkgs_storage_policy_identifier
        cluster_spec.ephemeral_storage_policy = tkgs_storage_policy_identifier
        # cluster_spec.login_banner = None
        # cluster_spec.master_dns_names = None
        cluster_spec.image_storage = self.cluster_object.ImageStorageSpec(tkgs_storage_policy_identifier)
        # cluster_spec.default_image_registry = None
        # cluster_spec.default_image_repository = None
        cluster_spec.default_kubernetes_service_content_library = self.content_library_name

        self.cluster_object.enable(self.cluster_name, cluster_spec)

        error_count = 0
        errors_to_tollerate = 10
        while True:
            my_cluster = self.cluster_object.get(self.cluster_name)
            if my_cluster.config_status == "RUNNING":
                break
            elif my_cluster.config_status == "ERROR":
                # It seems to randomly enter error states and then recover
                error_count += 1
                if error_count > errors_to_tollerate:
                    print("\n\n##### Massive fail! #####\n\n")
                    print(my_cluster.messages)
            sleep(5)

        self.module.exit_json(
            changed=True,
            namespace_cluster_vds_info = '{"TODO"}'
        )

    def state_update_cluster(self):
        self.module.exit_json(
            changed=True,
            namespace_cluster_vds_info = '{"TODO"}'
        )

    def state_disable_cluster(self):
        """
        Disable cluser

        """
        self.cluster_object.disable(self.cluster_name)
        self.module.exit_json(
            changed=True,
            namespace_cluster_vds_info=dict(
                msg="Cluster '%s' is disabled." % self.cluster_name,
                namespace_cluster_vds_info='{"TODO"}'
            )
        )


def main():
    argument_spec = VmwareRestClient.vmware_client_argument_spec()
    argument_spec.update(
        content_library_name=dict(type='str', required=False),
        cluster_name=dict(type='str', required=True),
        dns_search_domains=dict(type='list', required=False),
        dns_servers=dict(type='list', required=False),
        haproxy_ca_chain=dict(type='str', required=False),
        haproxy_management_ip=dict(type='str', required=False),
        haproxy_password=dict(type='str', required=False),
        haproxy_range_count=dict(type='int', required=False),
        haproxy_range_start_address=dict(type='str', required=False),
        haproxy_username=dict(type='str', required=False),
        management_port_group=dict(type='str', required=False),
        management_gateway=dict(type='str', required=False),
        management_starting_address=dict(type='str', required=False),
        management_netmask=dict(type='str', required=False),
        ntp_servers=dict(type='list', required=False),
        workload_gateway=dict(type='str', required=False),
        workload_portgroup=dict(type='str', required=False),
        workload_range_starting_ip=dict(type='str', required=False),
        workload_range_count=dict(type='int', required=False),
        workload_netmask=dict(type='str', required=False),
        services_cidr=dict(type='str', required=False),
        supervisor_size=dict(type='str', choices=['tiny', 'small', 'medium', 'large', 'xlarge'], required=False), 
        state=dict(type='str', choices=['present', 'absent'], default='present', required=False),
        storage_policy_name=dict(type='str', required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False,
                           required_if=(
                                        ('state', 'present', ['content_library_name', 'dns_servers', 'haproxy_ca_chain',
                                                              'haproxy_management_ip', 'haproxy_password', 'haproxy_range_count', 
                                                              'haproxy_range_start_address', 'haproxy_username',
                                                              'management_port_group', 'management_gateway', 
                                                              'management_starting_address', 'management_netmask',
                                                              'ntp_servers', 'workload_gateway', 'workload_portgroup',
                                                              'workload_range_starting_ip', 'workload_range_count',
                                                              'workload_netmask', 'services_cidr', 'supervisor_size',
                                                              'storage_policy_name'
                                                              ]),
                                       )
                          )

    vmware_namespace_cluster_manage = VmwareNamespaceClusterVdsManage(module)
    vmware_namespace_cluster_manage.process_state()


if __name__ == '__main__':
    main()
