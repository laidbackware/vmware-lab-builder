FROM ubuntu:24.04

ENV ANSIBLE_VERSION=2.16.3-0ubuntu2

ENV ANSIBLE_HOST_KEY_CHECKING=False

RUN set -xe \
    && echo "****** Install packages with apt ******" \
    && export DEBIAN_FRONTEND=noninteractive \
    && apt update \
    && apt install -y --no-install-recommends \
        ca-certificates iputils-ping python3-apt libarchive-tools sshpass \
        build-essential python3 python3-jmespath python3-setuptools \
        python3-pip python3-dev git curl ansible-core \
    \
    && ln --symbolic /usr/bin/python3 /usr/bin/python \
    \
    && echo "****** Installing OM CLI ******" \
    && arch=$(a=$(uname -m) && ([ $a = aarch64 ] || [ $a = arm64 ]) && printf arm64 || printf amd64) \
    && curl -L https://github.com/pivotal-cf/om/releases/download/7.9.0/om-linux-${arch}-7.9.0 --output /usr/local/bin/om \
    && chmod +x /usr/local/bin/om \
    \
    && echo "****** Installing Python modules ******" \
    && pip3 install pyvmomi netaddr \ 
        git+https://github.com/vmware/vsphere-automation-sdk-python.git --break-system-packages \
    \
    && echo "****** Adding community.vmware from Ansible Galaxy ******" \
    && ansible-galaxy collection install community.vmware:5.1.0 \
    \
    && echo "****** Adding vmware.avi from Ansible Galaxy ******" \
    && ansible-galaxy collection install vmware.alb:22.1.4 \
    \
    && echo "****** Adding ansible.utils from Ansible Galaxy ******" \
    && ansible-galaxy collection install ansible.utils \
    \
    && echo "****** Adding community.crypto from Ansible Galaxy ******" \
    && ansible-galaxy collection install community.crypto \
    \
    && echo "****** Adding community.general from Ansible Galaxy ******" \
    && ansible-galaxy collection install community.general \
    \
    && echo "****** Adding ansible-for-nsxt from Github ******" \
    && ansible-galaxy collection install git+https://github.com/laidbackware/ansible-for-nsxt.git,upstream-fixes --force \
    \
    && echo "****** Cloning ansible-for-vsphere-tanzu ******" \
    && ansible-galaxy collection install git+https://github.com/laidbackware/ansible-for-vsphere-tanzu.git,ansible-galaxy \
    \
    && echo "****** Removing build tools ******" \
    && apt remove -y build-essential python3-pip python3-dev git curl \
    && apt autoremove -y \
    && rm -Rf /var/lib/apt/lists/* \
    && rm -Rf /usr/share/doc && rm -Rf /usr/share/man \
    && rm -rf /root/.cache/pip/ \
    && rm -rf /tmp/* \
    && apt-get clean
