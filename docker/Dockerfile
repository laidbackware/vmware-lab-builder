FROM alpine:latest
# python:3-alpine

ENV ANSIBLE_VERSION=2.10.*

#
# gawk tar gzip sed openssh sshpass py3-wheel
# setuptools 

RUN set -xe \
    && echo "****** Install system dependencies ******" \
    && apk add --no-cache --progress python3 openssl xorriso \
		ca-certificates git bash \  
	&& apk --no-cache add --virtual build-dependencies \
		python3-dev libxml2-dev libxslt-dev py3-pip build-base libffi-dev openssl-dev  \
	\
	&& echo "****** Install ansible and python dependencies ******" \
    && pip3 install --upgrade pip git+https://github.com/vmware/vsphere-automation-sdk-python.git  \
	&& pip3 install ansible==${ANSIBLE_VERSION} pyvmomi \
    \
    && echo "****** Remove unused system librabies ******" \
	&& apk del build-dependencies python3-dev libxml2-dev libxslt-dev py3-pip build-base libffi-dev openssl-dev \
	&& rm -rf /var/cache/apk/* 