# This image is currently broken!
FROM python:3.8-alpine

ENV ANSIBLE_VERSION=2.10.*

# python3
# gawk tar gzip sed openssh sshpass py3-wheel
# setuptools python3-dev py3-pip

# https://github.com/sgerrand/alpine-pkg-glibc/releases

RUN set -xe \
    && echo "****** Install system dependencies ******" \
    && apk add --no-cache --progress  openssl xorriso \
		ca-certificates git bash zlib-dev iputils \  
	&& apk --no-cache add --virtual build-dependencies \
		 libxml2-dev libxslt-dev  build-base libffi-dev openssl-dev  \
	\
	&& echo "****** Install ansible and python dependencies ******" \
    && pip3 install --upgrade pip git+https://github.com/vmware/vsphere-automation-sdk-python.git  \
	&& pip3 install ansible==${ANSIBLE_VERSION} pyvmomi requests \
	\
	&& echo "****** Installing glibc ******" \
	&& wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub \
	
	\
	&& echo "****** Remove unused system librabies ******" \
    && apk del build-dependencies  \
	&& rm -rf /var/cache/apk/*  \
	&& rm -rf /root/.cache/pip/*  \

# && sed -i "s/'6.6.0']/'6.6.0', '7.0.0']/g" /usr/lib/python3.*/site-packages/ansible_collections/community/vmware/plugins/modules/vmware_dvswitch.py

# libxml2-dev libxslt-dev build-base libffi-dev openssl-dev

# && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-2.32-r0.apk \
# 	&& wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-bin-2.32-r0.apk \
# 	&& wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.32-r0/glibc-i18n-2.32-r0.apk \
# 	&& apk add glibc-2.32-r0.apk glibc-bin-2.32-r0.apk glibc-i18n-2.32-r0.apk \
# 	&& /usr/glibc-compat/bin/localedef -i en_US -f UTF-8 en_US.UTF-8 \