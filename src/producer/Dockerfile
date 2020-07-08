FROM ubuntu
ADD ./config.json /root/
ADD ./producer.py /root/
ADD ./requirements.txt /root/
RUN apt update && apt install -y python3.8 && apt install -y python3-pip
RUN pip3 install -r /root/requirements.txt
CMD ["/usr/bin/python3", "/root/producer.py"]
