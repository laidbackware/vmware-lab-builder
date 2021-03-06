FROM ubuntu:20.04

ENV ANSIBLE_VERSION=2.10.*

ENV ANSIBLE_LIBRARY=/repos/ansible-for-nsxt:/repos/ansible-for-vsphere-tanzu
ENV ANSIBLE_MODULE_UTILS=/repos/ansible-for-nsxt/module_utils
ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN set -xe \
    && echo "****** Install packages with apt ******" \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt install -y --no-install-recommends \
        ca-certificates iputils-ping python3-apt libarchive-tools sshpass \
        build-essential python3 python3-jmespath python3-setuptools \
        python3-pip python3-dev git  \
    \
    && echo "****** Installing Python modules ******" \
    && pip3 install ansible pyvmomi netaddr \
        git+https://github.com/vmware/vsphere-automation-sdk-python.git \
    \
    && echo "****** Adding community.vmware from Ansible Galaxy ******" \
    && ansible-galaxy collection install community.vmware:1.8.0 \
    \
    && echo "****** Cloning ansible-for-nsxt ******" \
    && mkdir /repos \
    && git clone https://github.com/vmware/ansible-for-nsxt.git /repos/ansible-for-nsxt \
    \
    && echo "****** Cloning ansible-for-vsphere-tanzu ******" \
    && git clone https://github.com/laidbackware/ansible-for-vsphere-tanzu.git /repos/ansible-for-vsphere-tanzu \
    \
    && echo "****** Removing build tools ******" \
    && apt remove -y build-essential python3-pip python3-dev git \
    && apt autoremove -y \
    && rm -Rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && rm -rf /root/.cache/pip/ \
    && rm -rf /tmp/* \
    && apt-get clean \
