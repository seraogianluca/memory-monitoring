import time
import paramiko
import requests 
import json
from datetime import datetime


HOSTS = [
    ("172.16.2.46", "root", "tonno"),
    ("172.16.1.133", "root", "matilde"),
    ("172.16.1.210", "root", "lorenzo"),
    ("172.16.1.211", "root", "bifecco")
]

GNOCCHI_URL = 'http://'
GNOCCHI_URL_POST = "/v1/batch/metrics/measures"

def get_memory_info(host):
    """
        Perform an ssh request to the host, 
        perform the "free -m" command and get the memory usage percentage.
        -------
        params:
            host: (hostname, user, password)
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host[0],username=host[1],password=host[2])
    stdin, stdout, stderr = ssh_client.exec_command('free -m')

    memoryData = stdout.read().decode("utf-8") 
    ssh_client.close()
    split =  memoryData.split()
    now = datetime.now()
    timestamp = str(datetime.now())
  
    return {
        "timestamp" : timestamp,
        "memory percentage": round(int(split[8])/int(split[7]) * 100, 2)  
    }


def post_request(body):
    """
        Push the data to gnocchi db.
        ------------
        params:
            body: post body data
    """
    headers={
        'Content-Type':'application/json'
    }
    response = requests.post(url = GNOCCHI_URL_POST, data=body, headers=headers)

    # extracting response text
    pastebin_url = response.text 
    print("The pastebin URL is:%s"%pastebin_url) 
    

if __name__ == "__main__":
    frequency = 30 
    start_time = time.time()
    while (time.time() - start_time) <= 120:
        measures = 4 # Number of measures
        batch = {HOSTS[0][0] : [], HOSTS[1][0]: [], HOSTS[2][0]: [], HOSTS[3][0]: []}
        for host in HOSTS:
            batch[host[0]].append(get_memory_info(host))
        body = json.dumps(batch)
        # post_request(body)
        print('body ' + body)
        time.sleep(frequency)