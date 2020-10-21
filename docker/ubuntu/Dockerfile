FROM ubuntu:20.04

ENV ANSIBLE_VERSION=2.10.*

RUN set -xe \
    && echo "****** Install system dependencies ******" \
    && apt update \
    && apt install -y --no-install-recommends \
         python3 xorriso ca-certificates iputils-ping \
    \
    && echo "****** Install Python dependencies ******" \
    && apt install -y --no-install-recommends \
       python3-setuptools build-essential   \
       python3-pip python3-dev git  \
    \
    && echo "****** Installing Python modules ******" \
    && pip3 install ansible pyvmomi  git+https://github.com/vmware/vsphere-automation-sdk-python.git \
    \
    && echo "****** Removing build tools ******" \
    && apt remove -y build-essential python3-setuptools python3-pip python3-dev git \
    && apt autoremove -y \
    && rm -Rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && rm -rf /root/.cache/pip/ \
    && apt-get clean \
    && echo "***** Updating vmware_dvswitch.py to enable creation of vds 7.0 ****" \
    && sed -i "s/'6.6.0']/'6.6.0', '7.0.0']/g" /usr/local/lib/python3.*/dist-packages/ansible_collections/community/vmware/plugins/modules/vmware_dvswitch.py
