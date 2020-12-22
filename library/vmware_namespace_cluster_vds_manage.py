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
    haproxy_management_port: "5556"
    haproxy_password: haproxy
    haproxy_username: password_here
    haproxy_range_cidrs: ["172.31.0.128/26"]
    management_port_group: routed-pg
    management_gateway: "192.168.0.1"
    management_starting_address: "192.168.0.174"
    management_netmask: "255.255.252.0"
    management_address_count: 5
    ntp_servers: ["192.168.0.1"]
    workload_gateway: "172.31.0.1"
    workload_portgroup: private-pg
    # workload_range_starting_ip: "172.31.0.3"
    # workload_range_count: 40
    workload_range_cidrs: ["172.31.0.32/27"]
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

import uuid, ipaddress
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
        self.vsphere_api_object_mapping = {
            'network': self.api_client.vcenter.Network,
            'cluster': self.api_client.vcenter.Cluster,
            'policy': self.api_client.vcenter.storage.Policies
        }
        self.cluster_name = self.params.get('cluster_name')
        self.cluster_id = self.get_object_by_name(self.cluster_name, 'cluster')
        self.content_library_name = self.params.get('content_library_name')
        self.dns_search_domains = self.params.get('dns_search_domains')
        self.dns_servers = self.params.get('dns_servers')
        self.haproxy_ca_chain = self.params.get('haproxy_ca_chain')
        self.haproxy_management_ip = self.params.get('haproxy_management_ip')
        self.haproxy_management_port = self.params.get('haproxy_management_port')
        self.haproxy_password = self.params.get('haproxy_password')
        self.haproxy_range_cidrs = self.params.get('haproxy_range_cidrs')
        self.haproxy_username = self.params.get('haproxy_username')
        self.management_address_count = self.params.get('management_address_count')
        self.management_netmask = self.params.get('management_netmask')
        self.management_gateway = self.params.get('management_gateway')
        self.management_port_group = self.params.get('management_port_group')
        self.management_starting_address = self.params.get('management_starting_address')
        self.ntp_servers = self.params.get('ntp_servers')
        self.services_cidr = self.params.get('services_cidr')
        self.storage_policy_name = self.params.get('storage_policy_name')
        self.supervisor_size = self.params.get('supervisor_size')
        self.workload_gateway = self.params.get('workload_gateway')
        self.workload_netmask = self.params.get('workload_netmask')
        self.workload_portgroup = self.params.get('workload_portgroup')
        self.workload_range_cidrs = self.params.get('workload_range_cidrs')

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
        Check if Workload Management is enabled for a specific cluster
        Returns: 'present' if workload management is enabled or configured, else 'absent'
        """
        try:
            existing_cluster_status = self.cluster_object.get(self.cluster_id).config_status
            if existing_cluster_status == "RUNNING" or existing_cluster_status == "ERROR":
                return 'present'
            elif existing_cluster_status == "CONFIGURING" and desired_state == "absent":
                return 'present'
            else:
                self.module.fail_json(msg="Operation cannot continue. Cluster [%s] is currently in state %s" % (self.cluster_id, existing_cluster_status))
        except Exception:
            return 'absent'

    def state_exit_unchanged(self):
        """
        Return unchanged state

        """
        self.module.exit_json(changed=False)

    # Checks if a CIDR is valid
    def check_cidr(self, cidr, purpose):
        try:
            ipaddress.ip_network(cidr)
        except ValueError:
            self.module.fail_json(msg="%s cidr %s is invalid" % (purpose, cidr))

    # Takes a list of cidr strings and return a list of IPRange objects
    def build_range_list(self, cidr_list, purpose):
        ip_ranges = []
        for cidr in cidr_list:
            self.check_cidr(cidr, purpose)
            cidr_split = cidr.split('/')
            ip_ranges.append(IPRange(address=cidr_split[0], 
                                           count=int(cidr_split[1])))
        return ip_ranges

    # Gets the internal identifies of an object
    def get_object_by_name(self, object_name, object_type):
        object_list = self.vsphere_api_object_mapping[object_type].list()
        for item in object_list:
            if item.name == object_name:
                object_id = eval("item.%s" % object_type)
                return object_id
        self.module.fail_json(msg="%s named %s was not found" % (object_type, object_name))

    def state_enable_cluster(self):
        """
        Enable workload management on a cluster using vSphere networking.
        """
        tkgs_storage_policy_identifier = self.get_object_by_name(self.storage_policy_name, 'policy')

        management_network_range = self.cluster_object.Ipv4Range()
        management_network_range.starting_address = self.management_starting_address
        management_network_range.address_count = self.management_address_count
        management_network_range.subnet_mask = self.management_netmask
        management_network_range.gateway = self.management_gateway

        management_network_spec = self.cluster_object.NetworkSpec()
        management_network_spec.network = self.get_object_by_name(self.management_port_group, 'network')
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
        haproxy_ranges = self.build_range_list(self.haproxy_range_cidrs, "haproxy_range_cidrs")
        loadbalancer_spec.address_ranges = haproxy_ranges
        loadbalancer_spec.provider = "HA_PROXY"
        loadbalancer_spec.ha_proxy_config_create_spec = haproxy_spec

        self.check_cidr(self.services_cidr, "services_cidr")
        services_cidr_split = self.services_cidr.split('/')
        services_cidr = Ipv4Cidr(address=services_cidr_split[0], prefix=int(services_cidr_split[1]))

        workload_vsphere_network_spec = self.network_object.VsphereDVPGNetworkCreateSpec()
        workload_vsphere_network_spec.portgroup = self.get_object_by_name(self.workload_portgroup, "network")
        workload_ranges = self.build_range_list(self.workload_range_cidrs, "workload_range_cidr")
        
        workload_vsphere_network_spec.address_ranges = workload_ranges
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
        cluster_spec.image_storage = self.cluster_object.ImageStorageSpec(tkgs_storage_policy_identifier)
        cluster_spec.default_kubernetes_service_content_library = self.content_library_name

        self.cluster_object.enable(self.cluster_id, cluster_spec)

        error_count = 0
        errors_to_tollerate = 20
        while True:
            wip_cluster = self.cluster_object.get(self.cluster_id)
            if wip_cluster.config_status == "RUNNING":
                break
            elif wip_cluster.config_status == "ERROR":
                # Tollerate errors as it seems to randomly enter error states and then recover
                error_count += 1
                if error_count > errors_to_tollerate:
                    self.module.fail_json(msg="Enabling workload management on [%s] failed with error: %s" % (self.cluster_name, wip_cluster.messages))
            sleep(5)

        self.module.exit_json(
            changed=True,
            namespace_cluster_results = dict(
                msg="Cluster '%s' has had workload management enabled." % self.cluster_name,
                cluster_name=self.cluster_name,
                cluster_id=self.cluster_id,
                cluster_state="RUNNING"
            )
        )

    def state_update_cluster(self):
        self.module.exit_json(
            changed=False,
            namespace_cluster_vds_info = dict(msg='Updates not currently supporter')
        )

    def state_disable_cluster(self):
        """
        Disable cluser

        """
        self.cluster_object.disable(self.cluster_id)
        self.module.exit_json(
            changed=True,
            namespace_cluster_results=dict(
            msg="Cluster '%s' has had workload management enabled." % self.cluster_name,
                cluster_name=self.cluster_name,
                cluster_id=self.cluster_id,
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
        haproxy_management_port=dict(type='str', required=False, default='5556'),
        haproxy_password=dict(type='str', required=False),
        haproxy_range_cidrs=dict(type='list', required=False),
        haproxy_username=dict(type='str', required=False),
        management_address_count=dict(type='int', required=False, default=5),
        management_gateway=dict(type='str', required=False),
        management_netmask=dict(type='str', required=False),
        management_port_group=dict(type='str', required=False),
        management_starting_address=dict(type='str', required=False),
        ntp_servers=dict(type='list', required=False),
        workload_gateway=dict(type='str', required=False),
        workload_netmask=dict(type='str', required=False),
        workload_portgroup=dict(type='str', required=False),
        workload_range_cidrs=dict(type='list', required=False),
        services_cidr=dict(type='str', required=False),
        supervisor_size=dict(type='str', choices=['tiny', 'small', 'medium', 'large', 'xlarge'], required=False), 
        state=dict(type='str', choices=['present', 'absent'], default='present', required=False),
        storage_policy_name=dict(type='str', required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False,
                           required_if=(
                                        ('state', 'present', ['content_library_name', 'dns_servers', 'haproxy_ca_chain',
                                                              'haproxy_management_ip', 'haproxy_password', 
                                                              'haproxy_range_cidrs', 'haproxy_username',
                                                              'management_port_group', 'management_gateway', 
                                                              'management_starting_address', 'management_netmask',
                                                              'ntp_servers', 'workload_gateway', 'workload_portgroup',
                                                              'workload_range_cidrs',
                                                              'workload_netmask', 'services_cidr', 'supervisor_size',
                                                              'storage_policy_name'
                                                              ]),
                                       )
                          )

    vmware_namespace_cluster_manage = VmwareNamespaceClusterVdsManage(module)
    vmware_namespace_cluster_manage.process_state()


if __name__ == '__main__':
    main()
