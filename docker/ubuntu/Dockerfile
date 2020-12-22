   #  && echo "***** Updating vmware_dvswitch.py to enable creation of vds 7.0 ****" \
   #  && sed -i "s/'6.6.0']/'6.6.0', '7.0.0']/g" /usr/local/lib/python3.*/dist-packages/ansible_collections/community/vmware/plugins/modules/vmware_dvswitch.py
FROM ubuntu:20.04

ENV ANSIBLE_VERSION=2.10.*

ENV ANSIBLE_LIBRARY=/repos/ansible-for-nsxt
ENV ANSIBLE_MODULE_UTILS=/repos/ansible-for-nsxt/module_utils

RUN set -xe \
    && echo "****** Install system dependencies ******" \
    && apt update \
    && apt install -y --no-install-recommends \
         python3 ca-certificates iputils-ping python3-apt libarchive-tools \
    \
    && echo "****** Install Python dependencies ******" \
    && apt install -y --no-install-recommends \
       python3-setuptools build-essential   \
       python3-pip python3-dev git  \
    \
    && echo "****** Installing Python modules ******" \
    && pip3 install ansible pyvmomi netaddr \
         git+https://github.com/vmware/vsphere-automation-sdk-python.git \
    \
    && echo "****** Cloning modified vSphere Ansible repo ******" \
    && git clone --branch tkgs https://github.com/laidbackware/ansible-for-vsphere.git /tmp/ansible-for-vsphere \
    && cp -rf /tmp/ansible-for-vsphere/* /usr/local/lib/python3.*/dist-packages/ansible_collections/community/vmware/ \
    \
    && echo "****** Cloning ansible-for-nsxt ******" \
    && mkdir /repos \
    && git clone --branch vmware-lab-builder https://github.com/laidbackware/ansible-for-nsxt.git /repos/ansible-for-nsxt \
    \
    && echo "****** Removing build tools ******" \
    && apt remove -y build-essential python3-pip python3-dev git \
    && apt autoremove -y \
    && rm -Rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && rm -rf /root/.cache/pip/ \
    && rm -rf /tmp/* \
    && apt-get clean \