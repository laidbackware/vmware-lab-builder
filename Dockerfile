FROM ubuntu:20.04

RUN apt-get update
RUN apt-get -y install \
        xorriso \
        sshpass \
        python3-pip \
        git

RUN pip3 install \
    	ansible \
    	pyvmomi \
    	git+https://github.com/vmware/vsphere-automation-sdk-python.git

RUN mkdir /work
WORKDIR /work
