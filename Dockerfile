FROM ubuntu:20.04

RUN apt-get update

# ping is required by `vcsa-deploy`
RUN apt-get -y install \
        iputils-ping \
        xorriso \
        sshpass \
        python3-pip \
        git

RUN pip3 install \
    	ansible \
    	pyvmomi \
    	git+https://github.com/vmware/vsphere-automation-sdk-python.git

# Fix vmware_dvswitch.py library on filesystem ..
# TODO: Remove once fixed upstream
COPY fix_dvs_for_7.sh /tmp/
RUN /tmp/fix_dvs_for_7.sh

RUN mkdir /work
WORKDIR /work
