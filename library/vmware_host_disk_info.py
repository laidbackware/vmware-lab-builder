#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'author': 'Matt Proud'
}

DOCUMENTATION = '''
'''

EXAMPLES = '''
'''

RETURN = '''
'''

try:
    from pyVmomi import vim
except ImportError:
    pass

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.vmware.plugins.module_utils.vmware import vmware_argument_spec, PyVmomi, get_all_objs

class HostDiskInfo(PyVmomi):
    """Class to return host disk info"""

    def __init__(self, module):
        super(HostDiskInfo, self).__init__(module)
        cluster_name = self.params.get('cluster_name', None)
        esxi_host_name = self.params.get('esxi_hostname', None)
        self.hosts = self.get_all_host_objs(cluster_name=cluster_name, esxi_host_name=esxi_host_name)
        if not self.hosts:
            self.module.fail_json(msg="Failed to find host system.")

    def gather_host_disk_info(self):
        hosts_disk_info = {}
        for host in self.hosts:
            host_disk_info = []
            storage_system = host.configManager.storageSystem.storageDeviceInfo
            # Collect target lookup for naa devices
            lun_lookup = {}
            for lun in storage_system.multipathInfo.lun:
                key = lun.lun
                paths = []
                for path in lun.path:
                    paths.append(path.name)
                lun_lookup[key] = paths

            for disk in storage_system.scsiLun:
                canonical_name = disk.canonicalName
                try:
                    capacity = disk.capacity.block * disk.capacity.blockSize / 1073741824
                except AttributeError:
                    capacity = 0
                try:
                    device_path = disk.devicePath
                except AttributeError:
                    device_path = ""
                device_type = disk.deviceType
                display_name = disk.displayName
                disk_uid = disk.key
                disk_ctd = lun_lookup[disk_uid]
                
                disk_dict = {"capacity": capacity,
                                        "device_path": device_path,
                                            "device_type": device_type,
                                            "display_name": display_name,
                                            "disk_uid": disk_uid,
                                            "disk_ctd": disk_ctd,
                                            "canonical_name": canonical_name}
                host_disk_info.append(disk_dict)

            hosts_disk_info[host.name] = host_disk_info
        
        return hosts_disk_info



def main():
    """Main"""
    argument_spec = vmware_argument_spec()
    argument_spec.update(
        cluster_name=dict(type='str', required=False),
        esxi_hostname=dict(type='str', required=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[
            ['cluster_name', 'esxi_hostname'],
        ],
        supports_check_mode=True,
    )

    host_disk_mgr = HostDiskInfo(module)
    module.exit_json(changed=False, hosts_disk_facts=host_disk_mgr.gather_host_disk_info())


if __name__ == "__main__":
    main()