FROM ubuntu
ADD ./config.json /root/
ADD ./consumer.py /root/
RUN apt-get update && apt-get install -y python3.8
RUN apt update
RUN apt install -y python3-pip
RUN pip3 install paramiko
RUN pip3 install keystoneauth1
RUN pip3 install prettytable
CMD ["/usr/bin/python3", "/root/consumer.py"]
