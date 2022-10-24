FROM ubuntu:22.04

ENV ANSIBLE_VERSION=2.13.*

ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN set -xe \
    && echo "****** Install packages with apt ******" \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt install -y --no-install-recommends \
        ca-certificates iputils-ping python3-apt libarchive-tools sshpass \
        build-essential python3 python3-jmespath python3-setuptools \
        python3-pip python3-dev git \
    \
    && ln --symbolic /usr/bin/python3 /usr/bin/python \
    \
    && echo "****** Installing Python modules ******" \
    && pip3 install ansible pyvmomi netaddr requests \
        git+https://github.com/vmware/vsphere-automation-sdk-python.git \
    \
    && echo "****** Adding community.vmware from Ansible Galaxy ******" \
    && ansible-galaxy collection install community.vmware:3.0.0 \
    \
    && echo "****** Adding vmware.avi from Ansible Galaxy ******" \
    && ansible-galaxy collection install vmware.alb:21.1.5 \
    \
    && echo "****** Adding ansible-for-nsxt from Github ******" \
    && ansible-galaxy collection install git+https://github.com/vmware/ansible-for-nsxt.git,v3.2.0 \
    \
    && echo "****** Cloning ansible-for-vsphere-tanzu ******" \
    && ansible-galaxy collection install git+https://github.com/laidbackware/ansible-for-vsphere-tanzu.git,ansible-galaxy \
    \
    && echo "****** Removing build tools ******" \
    && apt remove -y build-essential python3-pip python3-dev git \
    && apt autoremove -y \
    && rm -Rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && rm -rf /root/.cache/pip/ \
    && rm -rf /tmp/* \
    && apt-get clean
